import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Utility.toolbox import find_repo_root
from genre_shifter import genre_shifter  # Assuming your class is saved in genre_shifter.py

# Set up project root
root = find_repo_root()

# Streamlit UI
st.title("Movie Genre Trope Comparison")

# User inputs
movie1 = st.text_input("Enter first movie:", "Alien")
movie2 = st.text_input("Enter second movie:", "Paddington2")
genre = st.selectbox("Select genre:", ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"])  # Add real genres
cutoff = st.slider("Number of top shifts to display", 5, 50, 100, 500)

# Function to generate the plot with two subplots
def plot_comparison(gs, genre, cutoff):
    fig, axes = plt.subplots(1, 2, figsize=(16, 12))  # Two subplots side by side

    # First plot: Movie1 relative to Movie2
    gs.ref_name, gs.comp_name = movie1, movie2
    gs.plot(genre, cutoff, ax=axes[0])
    axes[0].set_title(f"{movie1} vs {movie2}")

    # Second plot: Movie2 relative to Movie1
    # gs.reverse_comp_ref()
    # gs.plot(genre, cutoff, ax=axes[1])
    # axes[1].set_title(f"{movie2} vs {movie1}")

    plt.tight_layout()
    return fig

# Instantiate and process data
if st.button("Compare Movies"):
    gs = genre_shifter()
    gs.build_comp_ref_by_movie(movie1, movie2)
    
    # Generate double plot
    fig = plot_comparison(gs, genre, cutoff)
    st.pyplot(fig, use_container_width=True)
