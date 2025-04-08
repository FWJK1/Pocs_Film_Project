
## default python packages
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

## third party packages
import streamlit as st

## homebrew packages
from genre_troperator import GenreTroperator
from tropeogram_plotter import TropeogramPlotter
from Utility.toolbox import find_repo_root

root = find_repo_root()
movies = {
    "Alien" : "Data/trope_time_series/alien_tropes.csv",
    "Clueless" : f"{root}/Data/trope_time_series/clueless_tropes.csv"
}

def initialize_state(matrix, max_workers=max(1, os.cpu_count() - 4)):
    def trope_load(title, path):
        return title, GenreTroperator(matrix, path)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(trope_load, title, path) for title, path in movies.items()]
        results = {title: troperator for future in as_completed(futures) for title, troperator in [future.result()]}

    st.session_state.movies = results
    st.session_state.plotter = TropeogramPlotter()
    st.session_state.genres = next(iter(results.values())).genres
