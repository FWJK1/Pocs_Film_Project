## project code for ease
from Utility.toolbox import find_repo_root, log_time, eval_pd_data_string_literal
from Utility.genre_trope_matrix import build_prop_trope_matrix
root = find_repo_root()

## 3rd party libraries
import pandas as pd

## standard libraries
from collections import Counter


class GenreShifterData:
    def __init__(self, root):
        self.root = root
        self.matrix_df = self.load_matrix()
        self.tropeset = pd.read_csv(f"{root}/Data/movies-vs-tropes.csv", sep=';')
        self.tropeset['Tropes'] = self.tropeset['Tropes'].map(eval_pd_data_string_literal)

        ## at some point we will transition to having a dictionary of scoring matrices

    def load_matrix(self, file=None):
        file = file or f"{self.root}/Code/Utility/genre_trope_matrix.py"
        try:
            return pd.read_csv(file)
        except:
            return build_prop_trope_matrix(norm="num_movies")
        
    def build_comp_ref_with_time(self, ref_file, ref_name, comp_file=None, comp_name=None):
        self.ref_name = ref_name
        self.ref_basis = self.build_with_time(ref_file)

        if comp_file:
            self.comp_name = comp_name
            self.comp_basis = self.build_with_time(comp_file)
        else:
            self.comp_name = self.ref_name
            self.comp_basis = self.ref_basis
  
    def build_with_time(self, file, tau=600):
        df = pd.read_csv(file)
        df['Trope'] = df['Trope'].str.replace(" ", '')
        df = df[df['Trope'].isin(self.matrix_df['Trope'])]  # Filter early
        df = df.merge(right=self.matrix_df, on='Trope', how='left')
        return self.scale_to_time(df, tau)

    def scale_to_time(self, df, tau=600, matrix=None):
        matrix = matrix or self.matrix_df

        ## explode out the active seconds for each trope
        end_second = df['End Time'].max()
        df['time'] = df.apply(lambda row: list(range(row['Start Time'], min(row['End Time'] + tau, end_second))), axis=1)
        df_exploded = df.explode('time').reset_index(drop=True)

        ## aggregate into two cols: trope has list of unique tropes; the other cols have sum of active tropes in that genre (matrix scores the genre of each trope)
        genres = [col for col in matrix.columns if col != 'Trope']
        df_grouped = df_exploded.groupby('time').agg({
            'Trope': lambda x: list(set(x)),
            **{col: 'sum' for col in genres}
        }).reset_index()

        ## normalize the values
        df_grouped['total'] = df_grouped[genres].sum(axis=1)
        for col in genres:
            df_grouped[col] = df_grouped[col] / df_grouped['total']

        ## scale the time and return
        df_grouped['time'] = df_grouped['time'] / end_second
        return df_grouped.drop(columns=['total'])


    def make_timeless_df(self, name, matrix=None):
        matrix = matrix or self.matrix_df
        ## make a frame of the counts for the movies
        df = self.tropeset[self.tropeset['Movie'] == name]['Tropes']
        trope_counts = Counter(trope for tropes in df for trope in tropes)
        trope_df = pd.DataFrame(trope_counts.items(), columns=['Trope', 'Value'])

        ## score the frame and return
        trope_df = trope_df.merge(right=matrix, on='Trope', how='left').drop(columns='Value')
        return trope_df.dropna()

    def process_and_merge_tropes(self, df, matrix=None):
        matrix = matrix or self.matrix_df
        tropes = df['Trope'].explode().str.replace(" ", '').drop_duplicates()
        return pd.DataFrame({'Trope': tropes}).merge(matrix, on='Trope')

def slice_times_and_average(self, ref_range, comp_range):
    ## get names
    ref_label = f"{self.ref_name} from {ref_range[0]*100:.0f}% to {ref_range[1]*100:.0f}%"
    comp_label = f"{self.comp_name} from {comp_range[0]*100:.0f}% to {comp_range[1]*100:.0f}%"

    # get ranges
    ref = self.ref_basis[self.ref_basis['time'].between(*ref_range)]
    comp = self.comp_basis[self.comp_basis['time'].between(*comp_range)]

    # return, processesing frames in range as needed.
    return ref_label, self.process_and_merge_tropes(ref), comp_label, self.process_and_merge_tropes(comp)