import ast
import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from letterboxdpy.movie import Movie
from datetime import datetime
import concurrent.futures
import requests
import numpy as np
import random
import time
import Utility.toolbox as tb

root = tb.find_repo_root()

def fk_get_url(movie):
    try:
        return movie.get('url')
    except Exception as e:
        print(movie, e)
        return "None" 

def get_actor_roles(url):
    actors, roles = [], [] #setup storage
    html = tb.get_parsed_page(url)
    cast_list = html.find('div', class_='cast-list text-sluglist') #find the castlist section

    if cast_list:
        actor_tags = cast_list.find_all('a', href=True)
        for tag in actor_tags:
            if "/actor/" in tag['href']:  # Check if the href contains "/actor/"
                try:
                    actor_name = tag.text
                    role = tag['title']
                    
                    actors.append(actor_name)
                    roles.append(role)
                except Exception as e:
                    actor_name = tag.text
                    role = None
        return actors, roles
    else:
        print(f"No dice for {url}, {cast_list}. Double check.")
        return [], []

def process_movie_NER(url):
    time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
    return get_actor_roles(url)

def get_NER_all(data, chunksize=100, begin=0, length=None, output_file=None):
    df = data.copy()

    if not output_file:
        output_file = f'{root}/Data/2020_trope_data/Scraped_Data/actors_roles.csv'

    if not length:
        length = len(df)

    print(f"Scraping actors and roles for movies from {begin} to {length} with chunksize={chunksize}")
    
    # Parallelizing with ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for start in range(begin, length, chunksize):
            current_time = datetime.now()
            print(f"started {start} to {start + chunksize}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))
            chunk = df.iloc[start: start + chunksize].copy()

            chunk['actors'] = [[] for _ in range(len(chunk))]  # Initialize with empty lists
            chunk['roles'] = [[] for _ in range(len(chunk))]   # Initialize with empty lists

            
            # Submit tasks for fetching actors and roles, and store index with results
            # we need index to make sure the data is aligned despite running in parallel.
            futures = {index: executor.submit(process_movie_NER, url) for index, url in chunk['url'].items()} 

            for index, future in futures.items():
                actors, roles = future.result()
                # print(index, actors, roles)

                # Directly assign the actors and roles to the correct index in the chunk
                chunk.at[index, 'actors'] = actors ## note we use .at instead of .loc
                chunk.at[index, 'roles'] = roles


            # Write results to CSV after each chunk
            chunk.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)

            current_time = datetime.now()
            print(f"finished {start} to {start + chunksize}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))

    
    print(f"Scraped all actors and roles from {begin} to {length} with chunksize={chunksize}")

# Run the actual code:
df = pd.read_csv(f"{root}/Data/2020_trope_data/HIT_letterboxd_link_movies.csv")
df['Movie'] = df['Movie'].apply(tb.fk_apply_literal)
df['url'] = df['Movie'].apply(lambda x : fk_get_url(x))
get_NER_all(df, begin=int(input("Enter Beginning Line: ")))
