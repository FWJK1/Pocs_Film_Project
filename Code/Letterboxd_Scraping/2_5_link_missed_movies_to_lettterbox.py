import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from letterboxdpy.movie import Movie
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from Utility.toolbox import find_repo_root

root = find_repo_root()


## define the func 
def get_Movies_all(df, chunk_size=50, begin=0, length=None,
                   output_file=f'{root}/Data/2020_trope_data/letterboxd_link_movies.csv',
                    missed_output_file=f'{root}/Data/2020_trope_data/missed_letterboxd_links.csv',
                   sleeptime=1):
    
    if not length:
        length = len(df)


    print(f"Linking Movies: {begin} to {length}")

    all_movies = []  # To collect all movie results
    missed_movies = []

    with sync_playwright() as p:
        # Launch browser and set up headless option
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Process the DataFrame in chunks
        for start in range(begin, length, chunk_size):
            current_time = datetime.now()
            print(f"started chunk {start} to {start + chunk_size}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))

            chunk = df.iloc[start:start + chunk_size].copy()
            urls = chunk['letterboxd_search']

            for i, url in enumerate(urls):
                time.sleep(sleeptime)  # Time to wait between requests (if any)
                try:
                    page.goto(url)
                except Exception as e:
                    print(f"error with {url}: {e}")

                html_source = page.content()
                soup = BeautifulSoup(html_source, 'html.parser')

                # Get elements from soup and append them into the list
                try:
                    first_instance = soup.find('a', href=lambda href: href and href.startswith('/film/'))
                    if first_instance:
                        title = first_instance['href'].rstrip('/').split('/')[-1]
                        movie = Movie(title)  # Assuming Movie is defined elsewhere
                        all_movies.append((url, movie))
                    else:
                        # we didn't get the movie. So we save it in the missing list.
                        missed_movies.append(url)
                        print(f"Line {i} in block. No results on page for {url}. Try other year maybe.")
                        
                except Exception as e:
                    missed_movies.append(url)
                    print(f"{url} not found. Try other year maybe. Error: {e} Line{i}")

                # Save to CSV every chunk_size results processed
                if len(all_movies) % chunk_size == 0:

                    # Create a temporary DataFrame and append to CSV
                    temp_df = pd.DataFrame(all_movies, columns=['letterboxd_search', 'Movie'])
                    temp_df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)
                    all_movies = []  # Reset the list after saving

                    
                    # Do the same for the missing movies in a separate frame to re-search later
                    temp_df = pd.DataFrame(missed_movies, columns=['letterboxd_search'])
                    temp_df.to_csv(missed_output_file, mode='a', header=not pd.io.common.file_exists(missed_output_file), index=False)
                    missed_movies = []  # Reset the list after saving
                    print(f"finished chunk {start} to {start + chunk_size}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))

        # Save any remaining results / misses
        if all_movies:
            temp_df = pd.DataFrame(all_movies, columns=['letterboxd_search', 'Movie'])
            temp_df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)

            temp_df = pd.DataFrame(missed_movies, columns=['letterboxd_search'])
            temp_df.to_csv(missed_output_file, mode='a', header=not pd.io.common.file_exists(missed_output_file), index=False)
            print(f"finished chunk {start} to {start + chunk_size}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))

                          
        # Clean up
        browser.close()
        print(f"Linked  Movies: {begin} to {length}")

    return df


## Read in Dataframe 
df = pd.read_csv(f"{root}/Data/2020_trope_data/MISSED_letterboxd_link_movies.csv")
df['letterboxd_search'] = df['letterboxd_search'].str.replace('!', '', regex=False)



## run the function ##
get_Movies_all(
    df, chunk_size=50, begin=int(input("Enter Begin Line: ")), length=None,
    sleeptime=2, output_file=f'{root}/Data/2020_trope_data/HIT_letterboxd_link_movies.csv',
    missed_output_file=f'{root}/Data/2020_trope_data/round2_MISSED_letterboxd_link_movies.csv',
)
print("Movies linked.")
