import pandas as pd 
import re
from Utility.toolbox import find_repo_root
root = find_repo_root()


def clean_second(t):
    parts = list(map(int, re.findall(r'\d+', str(t))))
    if len(parts) == 1:
        return parts[0] * 60
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0  

def file_cleaner(file):
    df = pd.read_csv(file, encoding='latin1')
    df[['Start Time', 'End Time']] = df[['Start Time', 'End Time']].map(clean_second)
    df.to_csv(file, index=False)
    

if __name__ == "__main__":
    file = f"{root}/Data/trope_time_series/Fellowship_of_the_Ring_filled.csv"
    file_cleaner(file)