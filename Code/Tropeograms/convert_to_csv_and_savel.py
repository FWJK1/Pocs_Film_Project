import pandas as pd 
from Utility.toolbox import find_repo_root

root = find_repo_root()

df = pd.read_csv(f"{root}/Code/Tropeograms/Alien_Tropes.tsv", delimiter='\t')

df.to_csv(f"{root}/Data/trope_time_series/alien_tropes.csv")

df = pd.read_csv(f"{root}/Data/trope_time_series/alien_tropes.csv")

print(df)
