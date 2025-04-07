## third party packages
import streamlit as st


## homebrew packages
from genre_troperator import GenreTroperator
from tropeogram_plotter import TropeogramPlotter
from Utility.toolbox import find_repo_root

root = find_repo_root()


def initialize_state(matrix):
    gt = GenreTroperator(matrix)
    gt_c= GenreTroperator(matrix, f"{root}/Data/trope_time_series/clueless_tropes.csv")

    st.session_state.movies = {
        "Alien" : gt, 
        "Clueless"  : gt_c
    }
    st.session_state.plotter = TropeogramPlotter()
    st.session_state.genres = gt.genres

    