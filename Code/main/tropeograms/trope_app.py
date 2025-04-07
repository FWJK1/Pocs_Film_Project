## python packages
import argparse

## third party packages
import streamlit as st



## homebrew packages
from streamlit_state_manager import initialize_state


## initializing streamlit state. 
# Ideally this calculates everything smoothly so we can move.
if "initialized" not in st.session_state:
    parser = argparse.ArgumentParser(description="Command Line config for tropeogram plotter")
    parser.add_argument('--matrix', type=str, default='prop', choices=['prop', 'tf_idf'], 
                    help="Choose how to evalute the genreness of a trope. The default is 'prop,' for proportional")
    args = parser.parse_args()
                    
    initialize_state(matrix=args.matrix)
    st.session_state.initialized = True


### Actual UI Elements ###
st.set_page_config(layout="wide")

## vars
genres = st.session_state.genres
gt = st.session_state.movies['Alien']
gt_c = st.session_state.movies['Clueless']
default_y_range = gt.get_y_range()


with st.sidebar: 
    st.header("Filtering A")
    selected_range = st.slider("Select Y-Range for all plots", default_y_range[0], default_y_range[1], 
                               value=(default_y_range[0], default_y_range[1]))
    bot, top = selected_range
    bot, top = bot-.01, top+.01
    tau_vals = [1, 60, 120, 600, 1200]
    
    num_plots = 5  # Number of plots
    tau_selections = []
    genre_selections = []
    
    for i in range(num_plots):
        st.subheader(f"Plot {i+1}")
        tau_selections.append(st.selectbox(f"Select Trope Decay for Plot {i+1}", tau_vals, index=0, key=f"tau_{i}"))
        genre_selections.append(st.selectbox(f"Select Genre for Plot {i+1}", genres, index=genres.index('Horror'), key=f"genre_{i}"))

cols = st.columns(num_plots)
for i, (col, tau, genre) in enumerate(zip(cols, tau_selections, genre_selections)):
    with col:
        snapshot = gt.snapshots[tau]
        config = {
            "y_range": (bot, top), 
            "tau" : tau
            }
        fig = st.session_state.plotter.plot_genre_snapshots(snapshot, genre, config=config)
        
        # Assign a unique key to each chart to prevent duplication issuess
        st.plotly_chart(fig, use_container_width=True, key=f"plot_{i}")


cols = st.columns(num_plots)
for i, (col, tau, genre) in enumerate(zip(cols, tau_selections, genre_selections)):
    with col:
        snapshot = gt_c.snapshots[tau]
        config = {
            "y_range": (bot, top), 
            "tau" : tau
            }
        fig = st.session_state.plotter.plot_genre_snapshots(snapshot, genre, config=config)
        
        # Assign a unique key to each chart to prevent duplication issuess
        st.plotly_chart(fig, use_container_width=True, key=f"plot_{i}*2")

