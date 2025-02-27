from transformers import DistilBertTokenizer, DistilBertModel
from sklearn.cluster import KMeans
import torch
import numpy as np
import pandas as pd
import fastparquet ## make sure environment has fastparquet and NOT pyarrow
import itertools
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pybktree import BKTree
import time 
import ast
import concurrent.futures
from datetime import datetime




import os

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
root = root.replace('\\', '/')


def combine_adjacent_blocks(text, block_pattern, print_pattern):
    # This pattern looks for occurrences of the block followed by the same block, and replaces them with a single block
    result = re.sub(rf'({block_pattern} {block_pattern})', print_pattern, text)
    return result


def split_names(names_list):
    split_name_list = []
    names_list = ast.literal_eval(names_list)  # Assuming names_list is a string representation of a list
    for name in names_list:
        parts = name.split()
        if len(parts) > 1:
            # Only take the first and last names
            first_name = parts[0].lower()
            last_name = parts[-1].lower()
            split_name_list.append(first_name)
            split_name_list.append(last_name)
        else:
            # If only one name is provided (e.g., a single first name), just add it
            split_name_list.append(parts[0].lower())
    
    return split_name_list


def split_review(review):
    # Replace slashes and periods with spaces to treat them as word delimiters
    review_cleaned = re.sub(r'[/.]', ' ', review)  # Replace slashes and periods with spaces
    
    # Remove possessive 's or ’s (e.g., John's -> John, Marielle’s -> Marielle)
    review_cleaned = re.sub(r"[’']s\b", '', review_cleaned)  # Handles both straight and curly apostrophes
    
    # Remove unwanted characters (non-alphanumeric, except for common punctuation)
    review_cleaned = re.sub(r'[^a-zA-Z0-9?!.;, ]', '', review_cleaned)
    
    # Split the cleaned string into words (spaces are already used as delimiters)
    words = review_cleaned.split()
    
    return words


import nltk
from nltk.corpus import words

# Load the list of common words in English
english_words = set(words.words())

def filter_names_from_dict(word_list):
    # Filter out any words that are in the dictionary
    return [word for word in word_list if word.lower() not in english_words]


from fuzzywuzzy import process
from collections import defaultdict
import ast

# Function to extract all words from reviews (vocabulary)
def extract_words_from_reviews(review_list):
    all_words = set()
    for review in review_list:
        words = split_review(review)  # Split the review into words
        all_words.update(map(lambda w: w.lower(), words))  # Normalize words to lowercase
    return all_words

# Function to add fuzzy matches for names against the vocabulary
def add_fuzzy_matches(names, vocabulary, placeholder, threshold=90, verbose=None):
    fuzzy_match_map = defaultdict(list)
    for name in names:
        matches = process.extract(name, vocabulary, limit=50)  # Get the top 30 fuzzy matches for each name
        if verbose==2: print(name, " : ", matches)
        for match, score in matches:
            if score >= threshold:  # Only accept matches above the threshold
                fuzzy_match_map[match.lower()].append(placeholder)
            else:
                break  # Stop matching once a score below the threshold is found
    if verbose: print(fuzzy_match_map)
    return fuzzy_match_map



def replace_title_in_review(title, review, threshold=80):
    # We use a regular expression to find potential title occurrences (case-insensitive)
    words = review.split()
    
    # Check each word to see if it fuzzy matches the title, and replace it if it does
    modified_review = []
    i = 0
    while i < len(words):
        word = words[i]
        
        # Check fuzzy match of the word with the title, allow for punctuation in between
        sentence_chunk = " ".join(words[i:i+len(title.split())])  # Grab chunk based on title length
        
        # If the chunk is similar enough to the title, replace it
        score = fuzz.ratio(title.lower(), sentence_chunk.lower())
        if score >= threshold:
            modified_review.append("[TITLE]")
            i += len(sentence_chunk.split())  # Skip the matched chunk length
        else:
            modified_review.append(word)
            i += 1

    return " ".join(modified_review)





# Main function to replace actors, directors, roles in reviews with placeholders
def replace_actors_with_placeholder(review_list, actor_list, director_list, title, role_list, verbose=None):
    # Parse the review list (assuming it's a string representation of a list)
    review_list = ast.literal_eval(review_list)

    
    # Split the names into a list of individual names (case insensitive)
    actor_list = split_names(actor_list)
    director_list = split_names(director_list)
    role_list = filter_names_from_dict(split_names(role_list))

    # Extract vocabulary (words in all reviews)
    vocabulary = extract_words_from_reviews(review_list)

    # Generate fuzzy matches for actors, directors, and roles
    fuzzy_match_map = defaultdict(list)
    fuzzy_match_map.update(
        add_fuzzy_matches(actor_list, vocabulary, '[ACTOR]', threshold=95, verbose=verbose))
    fuzzy_match_map.update(
        add_fuzzy_matches(director_list, vocabulary, '[DIRECTOR]', threshold=95, verbose=verbose))
    fuzzy_match_map.update(
        add_fuzzy_matches(role_list, vocabulary, '[ROLE]', threshold=95, verbose=verbose))
    
    # Initialize list to store updated reviews
    updated_reviews = []

    # Iterate over each review in the review list
    for review in review_list:
        updated_words = []

        # Iterate through each word in the review
        for word in split_review(review):
            normalized_word = word.lower()

            # Check if the word matches any fuzzy match in the map
            if normalized_word in fuzzy_match_map:
                updated_words.append(fuzzy_match_map[normalized_word][0])  # Use the first match (placeholder)
            else:
                updated_words.append(word)  # No match, keep the original word

        # Join the updated words back into a single string
        updated_review = " ".join(updated_words)
        
        # Replace the title in the review
        updated_review = replace_title_in_review(title=title, review=updated_review)

        # Combine adjacent blocks of placeholders (if needed)
        updated_review = combine_adjacent_blocks(updated_review, r'\[ACTOR\]', "[ACTOR]")
        updated_review = combine_adjacent_blocks(updated_review, r'\[ROLE\]', "[ROLE]")
        updated_review = combine_adjacent_blocks(updated_review, r'\[DIRECTOR\]', "[DIRECTOR]")

        # Add the updated review to the list
        updated_reviews.append(updated_review)
        if verbose: print(f"{review}\n{updated_review}'\n'{'--' * 50}")

    # print(f"Parsed {title}")
    return updated_reviews




def get_NER_all(data, chunksize=100, begin=0, length=None, output_file=None):
    df = data.copy()

    if not output_file:
        output_file = f'{root}/Data/2020_trope_data/Scraped_Data/NER_cleaned.csv'

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

            chunk['NER_cleaned_data'] = [[] for _ in range(len(chunk))]  # Initialize with empty lists


            # Submit tasks for fetching comments and budget separately
            futures = {index: executor.submit(replace_actors_with_placeholder, reviews) for index, reviews in chunk['url'].items()} 


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


df = pd.read_csv(F"{root}/Data/2020_trope_data/Scraped_Data/merged_NER_scraped_data.csv", index_col=0)
get_NER_all(df)