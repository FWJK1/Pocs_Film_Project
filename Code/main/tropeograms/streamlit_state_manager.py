## third party packages
import streamlit as st


## homebrew packages
from genre_troperator import GenreTroperator
from tropeogram_plotter import TropeogramPlotter


def initialize_state(matrix):
    gt = GenreTroperator(matrix)
    st.session_state.movies = {
        "Alien" : gt
    }
    st.session_state.plotter = TropeogramPlotter()
    st.session_state.genres = gt.genres

    