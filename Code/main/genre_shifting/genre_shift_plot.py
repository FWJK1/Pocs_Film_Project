## project code for ease
from Utility.toolbox import find_repo_root, log_time, eval_pd_data_string_literal
from Utility.genre_trope_matrix import build_trope_matrix
root = find_repo_root()

## extra libraries
from matplotlib import pyplot as plt

class GenreShifterPlotter:
    def __init__(self, genre_shifter_data):
        self.data = genre_shifter_data

    def plot(self, genre, ref_avg, comp_avg, ref_name, comp_name, cutoff=None, ax=None, side='left'):
        ref_avg = ref_avg
        comp_avg = comp_avg

        self.shifts = self.data.comp.copy()
        self.shifts['shifts'] = (self.shifts[genre] - ref_avg) * (100 / (len(self.shifts) * abs(ref_avg - comp_avg)))
        self.shifts['shift_size'] = self.shifts['shifts'].abs()
        if cutoff:
            self.shifts = self.shifts.nlargest(cutoff, 'shift_size')
        self.shifts.sort_values(by='shift_size', inplace=True, ascending=False)

        shifts = list(self.shifts['shifts'])[::-1]
        tropes = list(self.shifts['Trope'])[::-1]

        if ax is None:
            ax = plt.gca()

        bar_colors = ['darkorange' if v >= 0 else 'cornflowerblue' for v in shifts]
        ax.barh(tropes, shifts, color=bar_colors, edgecolor='black')
        ax.set_xlabel(f'Shifts in {genre}')
        ax.set_title(f"{ref_name} ({ref_avg:.3f}) \nVs. \n{comp_name} ({comp_avg:.3f})")
        ax.tick_params(axis='y', labelsize=8)

        position_methods = {
            "left": (ax.yaxis.set_label_position, ax.yaxis.tick_left),
            "right": (ax.yaxis.set_label_position, ax.yaxis.tick_right),
        }
        label_pos, tick_pos = position_methods[side]
        label_pos(side)
        tick_pos()
        return ax

    def plot_two(self, movie1, movie2, genre, cutoff):
        fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="papayawhip")

        self.data.build_comp_ref_by_movie(movie1, movie2)
        self.plot(genre, self.data.ref[genre].mean(), self.data.comp[genre].mean(), self.data.ref_name, self.data.comp_name, cutoff, ax=axes[0])

        self.data.reverse_comp_ref()
        self.plot(genre, self.data.ref[genre].mean(), self.data.comp[genre].mean(), self.data.ref_name, self.data.comp_name, cutoff, ax=axes[1], side='right')

        plt.tight_layout()
        return fig

    def plot_comparison(self, genre, movie_file, movie_name, ref_range, comp_range):
        self.data.build_comp_ref_with_time(movie_file, movie_name)
        self.data.slice_times_and_average(ref_range, comp_range)
        fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="papayawhip")
        self.plot(genre, self.data.ref[genre].mean(), self.data.comp[genre].mean(), self.data.ref_name, self.data.comp_name, cutoff=50, ax=axes[0])
        self.data.reverse_comp_ref()
        self.plot(genre, self.data.ref[genre].mean(), self.data.comp[genre].mean(), self.data.ref_name, self.data.comp_name, cutoff=50, ax=axes[1], side='right')
        return fig
