import git
import ast 
import bs4 as BeautifulSoup
import requests

from datetime import datetime
from functools import wraps
import time


## printing stuff
def printline():
    print("---" * 50)


## file management
def find_repo_root():
    repo = git.Repo(search_parent_directories=True)
    root = repo.git.rev_parse("--show-toplevel")
    return root.replace("\\", "/")


## data structure management (for dicts inside of dataframes, etc)
def eval_pd_data_string_literal(x):
    """
    Evaluate a data string within a pandas frame literally (as dict, list, etc).
    Note, def not perfect
    """
    try:
        return ast.literal_eval(x)
    except Exception:
        # If parsing fails, check if the string is in the format "a,b,c"
        if isinstance(x, str) and ',' in x: 
            return [item.strip() for item in x.split(',')]
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


## accessing stuff we want a lot
def get_genres():
    with open(f"{find_repo_root()}/Data/liteweight/genre_list.txt", "r") as f:
        return f.read().splitlines() 

