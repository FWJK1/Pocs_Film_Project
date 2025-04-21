
## default python packages
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

## third party packages
import streamlit as st

## homebrew packages
from genre_troperator import GenreTroperator
from tropeogram_plotter import TropeogramPlotter
from Utility.toolbox import find_repo_root, get_genres

root = find_repo_root()
movies = {
    "Alien" : "Data/trope_time_series/alien_tropes.csv",
    "Clueless" : f"{root}/Data/trope_time_series/clueless_tropes.csv"
}

def get_range(troperators):
    ranges = [movie.get_y_range() for movie in troperators]
    mins = [range[0] for range in ranges]
    maxs = [range[1] for range in ranges]
    return min(mins), max(maxs)

def get_top_5(troperators):
    maxs = [troperator.top_5 for troperator in troperators]
    interleaved = [item for group in zip(*maxs) for item in group]
    seen = set()
    return  [x for x in interleaved if not(x in seen or seen.add(x))]

def initialize_state(matrix):
    
    tropers = {
        title: GenreTroperator(matrix=matrix, movie_path=path) for title, path in movies.items()
    }
    st.session_state.range = get_range(list(tropers.values()))
    st.session_state.ranked_genres = get_top_5(list(tropers.values()))
    st.session_state.movies = tropers

    st.session_state.plotter = TropeogramPlotter()
    st.session_state.genres = get_genres()

