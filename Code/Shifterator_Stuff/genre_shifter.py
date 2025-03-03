## project code for ease
from Utility.toolbox import find_repo_root, log_time, eval_pd_data_string_literal
root = find_repo_root()

## extra libraries
import pandas as pd
from matplotlib import pyplot as plt


class genre_shifter:
    def __init__ (self):
        ## make matrix df get coded up if we need it (set up imports, etc)
        self.matrix_df = pd.read_csv(f"{root}/Data/liteweight/genre_trope_matrix.csv")
        self.tropeset = pd.read_csv(f"{root}/Data/movies-vs-tropes.csv", sep=';')
        self.tropeset['Tropes'] = self.tropeset['Tropes'].apply(lambda x : eval_pd_data_string_literal(x))

    def build_comp_ref_with_time(self, ref_file, ref_name, comp_file=None, comp_name=None):
        self.ref_name = ref_name
        self.ref = self.build_with_time(ref_file)

        if comp_file:
            self.comp_name = comp_name
            self.comp = self.build_with_time(comp_file)
        else:
            self.comp_name = self.ref_name
            self.comp = self.ref

    def slice_times(self, ref_range, comp_range):
        self.ref_name += f"for {ref_range[0]} to {ref_range[1]}"
        self.comp_name +=f"for {comp_range[0]} to {comp_range[1]}"
        ref_range = range(ref_range[0], ref_range[1])
        comp_range = range(comp_range[0], comp_range[1])
        self.ref = self.ref[self.ref['time'].isin(ref_range)]
        self.comp = self.comp[self.comp['time'].isin(comp_range)]

    def build_with_time(self, file): ## needs debugging
        df = pd.read_csv(file)
        df['Trope'] = df['Trope'].apply(lambda x: x.replace(" ", ''))
        df = df.merge(right=self.matrix_df, on='Trope', how='left')
        df = df.drop(columns='Rough Occurence in movie').dropna()
        tau = 600
        end_second = df['End Time'].max()

        df['active_seconds'] = df.apply(lambda row: set(range(row['Start Time'], min(row['End Time'] + tau, end_second))), axis=1)
        self.scale_to_time(df)

    
    def scale_to_time(self, df):
        end_second = df['End Time'].max()
        time_df = pd.DataFrame({'time': range(0, end_second+1)})
       
        df = df.explode("active_seconds").reset_index(drop=True).merge(
            right=time_df,
            left_on='active_seconds',
            right_on='time',
            how='left')
        
        print(df)
        genres = [col for col in self.matrix_df.columns if col != 'Trope']

        df  = df.groupby('time').agg({
             'Trope': lambda x: list(set(x)),  # Keep as list
                **{col: 'sum' for col in genres}  # Sum all value columns dynamically
        }).reset_index()
        print(df)

        df['total'] = df[genres].sum(axis=1)
        for col in genres:
            df[f'Normalized {col}'] = df[col] / df['total']
        df.drop(columns='total', inplace=True)
        print(df)


    def reverse_comp_ref(self):
        self.ref_name, self.comp_name = self.comp_name, self.ref_name
        self.comp, self.ref = self.ref, self.comp



    def make_timeless_df(self, name):
        df = self.tropeset[self.tropeset['Movie'] == name].copy()
        df = df['Tropes'].apply(lambda x: pd.Series({value: 1 for value in x}))
        df = df.transpose().reset_index()
        df.columns = ['Trope', 'Value']
        df = df.merge(right=self.matrix_df, on='Trope', how='left').drop(columns='Value')
        return df

    def build_comp_ref_by_movie(self, ref_name, comp_name):
        self.ref_name = ref_name
        self.comp_name = comp_name
        self.ref = self.make_timeless_df(self.ref_name)
        self.comp = self.make_timeless_df(self.comp_name)


    def plot(self, genre, cutoff=None, ax=None):
        ref_avg = self.ref[genre].mean()
        comp_avg = self.comp[genre].mean()

        # gen shifts columns and cutoff to get only largest
        self.shifts = self.comp.copy()
        self.shifts['shifts'] = self.shifts[genre].apply(lambda x: x - ref_avg)
        self.shifts['shifts'] = self.shifts['shifts'].apply(lambda x : x * (100 / len(self.shifts) * abs(ref_avg - comp_avg)))
        self.shifts['shift_size'] = self.shifts['shifts'].apply(lambda x : abs(x))
        if cutoff:
            self.shifts = self.shifts.nlargest(cutoff, 'shift_size')
        self.shifts.sort_values(by='shift_size', inplace=True, ascending=False)

        shifts = list(self.shifts['shifts'])[::-1]
        tropes = list(self.shifts['Trope'])[::-1]
        
        ## actual plotting
        if ax is None:
            ax = plt.gca()
        bar_colors = ['darkorange' if v >= 0 else 'cornflowerblue' for v in shifts]

        ax.barh(tropes, shifts, color=bar_colors)
        ax.set_ylabel('Tropes')
        ax.set_xlabel(f'Shifts in {genre}')
        ax.set_title(f'{genre} Shifter: for {self.ref_name} vs {self.comp_name}')
        ax.text(0.13, 0.86, f"{genre} avg. Ref: {ref_avg.round(3)} Comp: {comp_avg.round(3)}")
        return ax


if __name__== "__main__":
    gs = genre_shifter()
    # gs.build_with_time(f"{root}/Data/trope_time_series/alien_tropes.csv")

    gs.build_comp_ref_by_movie("Alien", "Paddington2")  
    ax = gs.plot("Horror", cutoff=50)
    