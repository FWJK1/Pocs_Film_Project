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

# Setup git root
def find_repo_root(start_path):
    current_path = os.path.abspath(start_path)
    while True:
        if os.path.isdir(os.path.join(current_path, '.git')) or \
           os.path.isfile(os.path.join(current_path, 'README.md')):
            return current_path
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            break
        current_path = parent_path
    return None

root = find_repo_root(os.getcwd())
root = root.replace("\\", "/")

# Define Functions
def fk_apply_literal(x):
    try:
        return ast.literal_eval(x)
    except Exception as e:
        return None

def get_parsed_page(url: str) -> BeautifulSoup:
    headers = {
        "referer": "https://letterboxd.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

def fk_get_url(movie):
    try:
        return movie.get('url')
    except Exception as e:
        print(movie, e)
        return "None" 

def get_studio(url) -> str:
    try:
        page = get_parsed_page(url+ "details/")

        studio = []

        div = page.find("div", {"id": ["tab-details"], })
        a = div.find_all("a")

        for item in a:
            if item['href'][1:7] == 'studio':
                studio.append(item.text)

        # print(url, studio)
        return studio
    except Exception as e:
        print(url, e)
        return None

def process_movie_NER(url):
    time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
    return get_studio(url)

def get_NER_all(data, chunksize=100, begin=0, length=None, output_file=None):
    df = data.copy()

    if not output_file:
        output_file = f'{root}/Data/2020_trope_data/Scraped_Data/actors_roles_studios.csv'

    if not length:
        length = len(df)

    print(f"Scraping studios for movies from {begin} to {length} with chunksize={chunksize}")
    
    studios =[]

    # Parallelizing with ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        for start in range(begin, length, chunksize):
            current_time = datetime.now()
            print(f"started {start} to {start + chunksize}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))
            chunk = df.iloc[start: start + chunksize].copy()

            chunk['studio'] = [[] for _ in range(len(chunk))]  # Initialize with empty lists


            # Submit tasks for fetching comments and budget separately
            futures = {index: executor.submit(process_movie_NER, url) for index, url in chunk['url'].items()} 


            for index, future in futures.items():
                studio = future.result()

                # Directly assign the actors and roles to the correct index in the chunk
                chunk.at[index, 'studio'] = studio ## note we use .at instead of .loc

            # Write results to CSV
            chunk.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)

            # Clear the lists for the next chunk
            studios.clear()

            current_time = datetime.now()
            print(f"finished {start} to {start + chunksize}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))
    
    print(f"Scraped all studios from {begin} to {length} with chunksize={chunksize}")

# Run the actual code:
df = pd.read_csv(f'{root}/Data/2020_trope_data/Scraped_Data/actors_roles.csv')
get_NER_all(df, begin=int(input("Enter Beginning Line: ")))
