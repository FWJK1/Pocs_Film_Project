import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Utility.toolbox import find_repo_root, get_genres
from genre_shifter import genre_shifter  # Assuming your class is saved in genre_shifter.py

# Set up project root
root = find_repo_root()

# Streamlit UI
st.title("Movie Genre Trope Comparison")

# User inputs for movie selection and genre
movie1 = st.text_input("Enter first movie:", "Alien")
movie2 = st.text_input("Enter second movie:", "Paddington2")
genre = st.selectbox("Select genre:", get_genres())
cutoff = st.slider("Number of top shifts to display", 5, 50, 1)

# Instantiate and process data on button click
if st.button("Compare Movies"):
    gs = genre_shifter()
    fig = gs.plot_two(movie1, movie2, genre, cutoff)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
