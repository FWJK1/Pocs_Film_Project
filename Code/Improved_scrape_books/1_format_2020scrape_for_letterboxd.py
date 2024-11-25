import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from letterboxdpy.movie import Movie



info = """
##Run through these lines in the terminal before running the code the first time ## 

pip install nest_asyncio
pip install playwright
pip install beautifulsoup4
pip install letterboxdpy
pip install pandas 
 pip install lxml
python -m playwright install

# End Requirements #

"""

print(info)

import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from letterboxdpy.movie import Movie

def find_repo_root(start_path):
    """
    useful general function for finding the (first, closest) repo root so github file paths work the same on different machines 
    """
    current_path = os.path.abspath(start_path)
    
    while True:
        # Check for the existence of the .git directory or other indicators
        if os.path.isdir(os.path.join(current_path, '.git')) or \
           os.path.isfile(os.path.join(current_path, 'README.md')):
            return current_path
        
        parent_path = os.path.dirname(current_path)
        
        # Stop if we reach the root directory
        if parent_path == current_path:
            break
        
        current_path = parent_path

    return None  # Return None if not found

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