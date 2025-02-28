import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from letterboxdpy.movie import Movie
import git
from Utility.toolbox import find_repo_root

root = find_repo_root(os.getcwd())
root = root.replace("\\", "/")

## Replace the filepath with wherever you store the 2020 update trope dataset 
print("Reading in CSV to Dataframe")
df = pd.read_csv(f"{root}/Data/2020_trope_data/2020_updated_tropeset.csv") 
print("Dataframe initialized. Formatting.")

df = df[['NameIMDB', 'Year', 'Rating', 'Id']]

df['letterboxd_search'] = "https://letterboxd.com/search/" + df['NameIMDB'] + " " + df['Year'].astype(str) + '/'
df['letterboxd_search'] = df['letterboxd_search'].map(
    lambda x: str(x).replace(" ", "+"))

print("Dataframe formatted. Pushing to csv.")
df.to_csv(f"{root}/Data/2020_trope_data/letterboxd_search.csv")
print(f"Formatted data @ {root}/Data/2020_trope_data/letterboxd_search.cs")
print("Script complete. Now run script 2.")