import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import Utility.toolbox as tb
from Utility.genre_trope_matrix import build_trope_matrix
import plotly.graph_objects as go
import streamlit as st


root = tb.find_repo_root()

class GenreTroperator:
    def __init__(self):
        self.matrix  = build_trope_matrix()
        self.genres = tb.get_genres()

    def load_movie_data(self, path=f"{root}/Data/trope_time_series/alien_tropes.csv"):
        movie_tropes = pd.read_csv(path)
        movie_tropes['Trope'] = movie_tropes['Trope'].str.replace(" ", "")  # Convert to CamelCase
        movie_tropes = movie_tropes.merge(self.matrix, on='Trope', how='left')
        movie_tropes['Duration'] = movie_tropes['End Time'] - movie_tropes['Start Time']
        self.movie_tropes = movie_tropes
        self.snap_shots = self.build_snapshots()


    def build_snapshots(self, tau=600):
        df = self.movie_tropes.copy()
        max_second = df['End Time'].max()

        # Create 'active_seconds' and 'func_start' as sets for each row
        df['active_seconds'] = df.apply(lambda row: set(range(row['Start Time'], min(max_second, row['End Time'] + tau))), axis=1)
        df['func_start'] = df.apply(lambda row: set(range(row['Start Time'], min(max_second, row['Start Time'] + tau))), axis=1)

        # Adjust genre expectations for inverted/subverted cases
        df.loc[(df['Inverted?/Defied?'] == 'Yes') | (df['Averted/Subverted?'] == 'Yes'), self.genres] *= -1
        df = df[df['Setups?'] != 'Yes']

        snapshots = []
        for second in range(max_second):
            filtered_df = df[df['func_start'].apply(lambda x: second in x)]
            if not filtered_df.empty:
                tropes = filtered_df['Trope'].tolist()

                # Apply decay based on how much time has passed in 'tau'
                time_since_start = second - filtered_df['Start Time']
                decay_factor = 1 - (time_since_start / tau)  # Decay decreases as time progresses
                decay_factor = decay_factor.clip(lower=0) 
                
                # Apply decay to genre expectations
                total_genre_expectation = filtered_df[self.genres].multiply(decay_factor, axis=0).sum()
                total_genre_expectation /= total_genre_expectation.sum() or 1  # Normalize
                total_genre_expectation = total_genre_expectation.clip(lower=0)

            else:
                total_genre_expectation = pd.Series([0] * len(self.genres), index=self.genres)
                tropes = []

            snapshots.append([second] + total_genre_expectation.tolist() + [tropes])

        # Create the snapshot dataframe and add the 'total' column
        snapshots_df = pd.DataFrame(snapshots, columns=['second'] + self.genres + ['active_tropes'])
        snapshots_df['total'] = snapshots_df[self.genres].sum(axis=1)

        return snapshots_df