import pandas as pd
import numpy as np
from Utility.toolbox import find_repo_root

root = find_repo_root()

def build_trope_matrix():
    df = pd.read_csv(f"{root}/Data/liteweight/2020_genre_counts_by_trope.csv")
    genres = df.columns[2:29].tolist()
    all_tropes = df.iloc[:, 1].tolist()

    # Create the matrix with normalized genre percentages
    matrix_maker = []

    # Iterate through rows (excluding the first column, which is 'trope')
    for index, row in df.iloc[:, 2:29].iterrows():
        genre_counts = row.tolist()
        normalization = sum(genre_counts)

        try:
            # Normalize genre counts to percentages
            genre_percents = [genre_count / normalization for genre_count in genre_counts] if normalization > 0 else genre_counts
        except ZeroDivisionError:
            genre_percents = genre_counts  # Handle division by zero case

        matrix_maker.append(genre_percents)

    ## build the dataframe, transpose, save
    df_matrix = pd.DataFrame(np.array(matrix_maker).T, columns=all_tropes, index=genres)
    df_matrix_t = df_matrix.transpose()
    df_matrix_t.reset_index(names='Trope', inplace=True)
    df_matrix_t.to_csv(f"{root}/Data/liteweight/genre_trope_matrix.csv", index=False)
    return df_matrix_t