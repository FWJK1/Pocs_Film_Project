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
from playwright.sync_api import sync_playwright


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

def fk_movie_popular_reviews(movie, n=None) -> dict:
    try:
        base = movie.get('url')
    except Exception as e:
        return None
    urls = [base + "/reviews/by/activity"]
    if n:
        for i in range(2, n+1): 
            urls.append(base + f"/reviews/by/activity/page/{i}")
    ret = []
    for url in urls:
        page = get_parsed_page(url)
        film_details = page.find_all(class_='film-detail')
        for detail in film_details:
            curr = {}
            try:
                curr['stars'] = detail.select_one('.rating').get_text(strip=True)
            except:
                curr['stars'] = None
            try: 
                curr['review'] = detail.select_one('.body-text').get_text(strip=True)
            except:
                curr['review'] = None
            try:
                curr['date'] = detail.select_one('.date ._nobr').get_text(strip=True)
            except:
                curr['review'] = None
            ret.append(curr)
    return ret

def get_budget(movie) -> str:
    try:
        url = movie.get('url')
    except Exception as e:
        return None
    match = re.search(r"https?://(?:www\.)?letterboxd\.com/film/([^/]+)/?", url)
    match = match.group(1)
    url = f'https://letterboxd.com/whatsthebudget/film/{match}'
    page = get_parsed_page(url)
    budget_meta = page.find('meta', {'name': 'description'}) or page.find('meta', {'property': 'og:description'})
    if budget_meta and 'content' in budget_meta.attrs:
        return budget_meta['content']
    else:
        return None



def process_movie_data_comments(movie):
    time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
    return fk_movie_popular_reviews(movie, n=8)

def process_movie_data_comments(movie):
    time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
    
    # Use Playwright to scrape the page and expand the review
    with sync_playwright() as p:
        # Launch browser and open a new page
        browser = p.chromium.launch(headless=True)  # Set headless=True to run in the background
        page = browser.new_page()

        # Get the movie URL
        try:
            base_url = movie.get('url')
        except Exception as e:
            print(f"Error getting movie URL: {e}")
            return None

        # Go to the movie's reviews page
        page.goto(base_url + "/reviews/by/activity")

        # Wait for the "more" button to appear and click it to reveal the full review
        page.wait_for_selector('a.js-reveal')  # Wait for the "more" link to appear
        page.click('a.js-reveal')  # Click the "more" link to expand the review

        # Wait for the content to fully load after expansion
        page.wait_for_selector('.body-text')  # You may need to adjust this selector based on your structure

        # Get the expanded review content
        reviews = page.query_selector_all('.film-detail .body-text')
        reviews_data = []
        for review in reviews:
            text = review.inner_text().strip()
            reviews_data.append(text)

        # Close the browser after scraping the reviews
        browser.close()

        return reviews_data  # Return the expanded reviews as a list

def process_movie_data_budget(movie):
    time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
    return get_budget(movie)


def get_reviews_all(data, chunksize=50, begin=0, length=None, n=8, output_file=None):
    df = data.copy()
    df['Movie'] = df['Movie'].apply(lambda x: fk_apply_literal(x))

    if not output_file:
        output_file = f'{root}/Data/2020_trope_data/Scraped_Data/movie_n={n}_comments.csv'

    if not length:
        length = len(df)

    print(f"Scraping Comments for movies from {begin} to {length} with chunksize={chunksize}")
    
    results_comments = []
    results_budget = []

    # Parallelizing with ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for start in range(begin, length, chunksize):
            current_time = datetime.now()
            print(f"started {start} to {start + chunksize}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))
            chunk = df.iloc[start: start + chunksize].copy()

            chunk['Budget'] = [[] for _ in range(len(chunk))]  # Initialize with empty lists
            chunk['comments'] = [[] for _ in range(len(chunk))]   # Initialize with empty lists

            # Submit tasks for fetching comments and budget separately
            futures_comments = {index: executor.submit(process_movie_data_comments, movie) for index, movie in chunk['Movie'].items()} 
            futures_budget = {index: executor.submit(process_movie_data_budget, movie) for index, movie in chunk['Movie'].items()}

            # Collect results for comments and budget separately
            for index, future in futures_comments.items():
                    comments = future.result()
                # print(index, actors, roles)

                # Directly assign the actors and roles to the correct index in the chunk
                    chunk.at[index, 'comments'] = comments ## note we use .at instead of .loc


            for index, future in futures_budget.items():
                    budget = future.result()
                # print(index, actors, roles)

                # Directly assign the actors and roles to the correct index in the chunk
                    chunk.at[index, 'Budget'] = budget ## note we use .at instead of .loc


            # Write results to CSV
            chunk.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)

            current_time = datetime.now()
            print(f"finished {start} to {start + chunksize}  at  " + current_time.strftime("%Y-%m-%d %H:%M:%S"))
            print("--" * 50)
    
    print(f"Scraped all comments from {begin} to {length} with chunksize={chunksize}")

# Run the actual code:
df = pd.read_csv(f"{root}/Data/2020_trope_data/HIT_letterboxd_link_movies.csv")
get_reviews_all(df, n=10, length=100,
                begin=int(input("Enter Beginning Line: ")),
                output_file=f"{root}/Data/2020_trope_data/Scraped_Data/trial_movie_n=10_comments.csv")
