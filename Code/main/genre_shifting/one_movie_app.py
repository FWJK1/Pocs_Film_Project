import streamlit as st
import matplotlib.pyplot as plt
from Utility.toolbox import find_repo_root, get_genres
from genre_shifter import genre_shifter  # Assuming the class is saved in a separate file called `genre_shifter.py`

root = find_repo_root()

# Create the Streamlit app
def create_streamlit_app():
    st.title("Alien Movie Genre Comparison")
    st.write("Slice *Alien* into two segments and compare them based on selected genres.")

    # Initialize the genre_shifter class
    gs = genre_shifter()

    #  fixed Movie file and name for now 
    movie_file = f"{root}/Data/trope_time_series/alien_tropes.csv"
    movie_name = "Alien"

    genre = st.selectbox("Select a Genre", get_genres())

    # Define text input boxes for selecting ranges of the movie to compare
    ref_range_input = st.text_input("Reference Range (0% to 100%)", "0,50")
    comp_range_input = st.text_input("Comparison Range (0% to 100%)", "50,100")

    try:
        # Ensure the values are valid
        ref_start, ref_end = map(int, ref_range_input.split(","))
        comp_start, comp_end = map(int, comp_range_input.split(","))
        if not (0 <= ref_start < ref_end <= 100 and 0 <= comp_start < comp_end <= 100):
            st.error("Please enter valid ranges: start must be less than end, and values should be between 0 and 100.")
        else:
            # Convert ranges to decimals
            ref_range_decimals = (ref_start / 100, ref_end / 100)
            comp_range_decimals = (comp_start / 100, comp_end / 100)

            # Run the comparison and plot results when button is clicked
            if st.button("Compare"):
                fig = gs.plot_comparison(genre, movie_file, movie_name, ref_range_decimals, comp_range_decimals)
                st.pyplot(fig)

    except ValueError:
        st.error("Invalid input. Please enter two comma-separated integers for each range (e.g., 0,50).")

    

# Run the app
if __name__ == "__main__":
    create_streamlit_app()
