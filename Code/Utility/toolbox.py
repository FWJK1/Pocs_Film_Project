# import git
import ast 
import bs4 as BeautifulSoup
import requests
import os

from datetime import datetime
from functools import wraps
import time

## printing stuff
def printline():
    print("---" * 50)


## file management
def find_repo_root():
    import git
    repo = git.Repo(search_parent_directories=True)
    root = repo.git.rev_parse("--show-toplevel")
    return root.replace("\\", "/")

def nogit_find_repo_root(startpath):
    current_path = os.path.abspath(startpath) # Path started on
    while True:
        if os.path.isdir(os.path.join(current_path, '.git')) or os.path.isfile(os.path.join(current_path, 'README.md')): # If on git path, return it
            return current_path
        
        parent_path = os.path.dirname(current_path)

        if parent_path == current_path: # If current path is parent path, stop 
            break
        current_path = parent_path # Set current path to parent path, to check if git path again
    return None # If an issue arises 
# root = find_repo_root(os.getcwd()) # Good to set as a global variable 


## data structure management (for dicts inside of dataframes, etc)
def fk_apply_literal(x):
    try:
        return ast.literal_eval(x)
    except Exception as e:
        return None


## scraping specific
def get_parsed_page(url: str) -> BeautifulSoup:
    headers = {
        "referer": "https://letterboxd.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")


## time management
def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record start time
        printline()
        print(f"Started {func.__name__} at {get_current_time()}")
        result = func(*args, **kwargs)
        end_time = time.time()  # Record end time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"Finished {func.__name__} at {get_current_time()}")
        print(f"Total time elapsed: {elapsed_time:.4f} seconds")  # Print elapsed time
        printline()
        print("\n")
        return result
    return wrapper
