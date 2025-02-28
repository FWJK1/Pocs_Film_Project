import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import Utility.toolbox as tb
from genre_trope_matrix import build_trope_matrix
import plotly.graph_objects as go


root = tb.find_repo_root()

class GenreTroperator:
    def __init__(self):
        try:
            self.matrix = pd.read_csv(f"{root}/Data/liteweight/genre_trope_matrix.csv")
        except Exception as e:
            print(f"{e}, so rebuiding trope matrix")
            self.matrix  = build_trope_matrix()

    def load_movie_data(self, path=f"{root}/Code/Tropeograms/Alien_Tropes.tsv", delimiter='\t'):
        movie_tropes = pd.read_csv(path, delimiter=delimiter)
        movie_tropes['Trope'] = movie_tropes['Trope'].apply(lambda x: x.replace(" ", "")) ##convert to CamelCase
        movie_tropes = movie_tropes.merge(right=self.matrix, on='Trope', how='left',)
        movie_tropes['Duration'] = movie_tropes['End Time'] - movie_tropes['Start Time']
        self.movie_tropes = movie_tropes

        
if __name__ == "__main__":
    GT = GenreTroperator()
    GT.load_movie_data()
    print(GT.movie_tropes)