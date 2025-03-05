import streamlit as st
import plotly.graph_objects as go
from tropeogram import GenreTroperator
import pandas as pd

@st.cache_data
def load_and_process_data():
    GT = GenreTroperator()
    GT.load_movie_data()
    return GT

@st.cache_data
def get_cached_snapshots(_GT, tau):
    return _GT.build_snapshots(tau=tau)

def plot_genre_snapshots(df, selected_genre):
    fig = go.Figure()

    # Plot the selected genre line (smoothed)
    fig.add_trace(go.Scatter(
        x=df['second'],  
        y=df[selected_genre], 
        mode='lines',  
        name=selected_genre, 
        line=dict(width=2),  
    ))

    # Get tropes data and times
    tropes_data = []
    times = []
    labels = []
    
    seen_tropes = set()  # To track tropes that have already been plotted
    
    # Loop through all rows to check for first occurrence of tropes
    for idx, row in df.iterrows():
        tropes = row['active_tropes']
        if tropes:  # If there are any tropes at this point
            for trope in tropes:
                # Only plot the trope if it's the first occurrence
                if trope not in seen_tropes:
                    seen_tropes.add(trope)
                    times.append(row['second'])
                    tropes_data.append(row[selected_genre])
                    labels.append(trope)  # Use individual trope as label

    # Only plot tropes if there are any
    if tropes_data:
        fig.add_trace(go.Scatter(
            x=times,
            y=tropes_data,
            mode='markers',  # Only markers without text
            name='Tropes',  
            marker=dict(size=8, color='red', symbol='circle'),
            text=labels,  # Text will show up on hover
            hoverinfo='text',  # Only show text on hover
        ))

    fig.update_layout(
        title=f"Genre Makeup Over Time: {selected_genre}",
        xaxis_title="Time (seconds)",
        yaxis_title="Percentage Makeup",
        template="plotly_white",  
        showlegend=True, 
        width=1000,  
        height=800,  
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)

def main():
    GT = load_and_process_data()

    st.title("Genre Makeup Over Time")
    st.write("Explore how genre expectations evolve over time with different tropes.")

    genre_options = GT.genres
    selected_genre = st.selectbox("Select Genre", genre_options, index=genre_options.index('Horror'))

    tau_values = [1, 60, 600, 1200]
    tau = st.select_slider("Select Tau Value", options=tau_values, value=600)

    # Build snapshots (this will be cached based on tau value)
    df = get_cached_snapshots(GT, tau)

    plot_genre_snapshots(df, selected_genre)

if __name__ == "__main__":
    main()
