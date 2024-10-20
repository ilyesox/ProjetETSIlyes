#!/usr/bin/env python
import github  # Importing the GitHub library to interact with GitHub API
import logging  # For logging messages and errors
import urllib.parse  # To parse and create URLs
import requests  # For making HTTP requests
import time  # For handling time-related tasks, like sleeping
import csv  # For CSV file operations
import datetime  # For handling date and time data
from github import Github  # Importing specifically the Github class from github library

# Constants for the file paths
LOG_FILE = "./github_collect.log"
OUTPUT_FILE = './saver/output.csv'

# GitHub API tokens used for authentication to avoid rate limits
GITHUB_API_TOKENS = [
    # Replace these with actual tokens
]

# Constants for setting up the search query parameters
ITEM_PER_PAGE = 100
SEARCH_QUERY = "extension:tf"
PARAMS = {"q": SEARCH_QUERY, "sort": "stars", "order": "desc", "per_page": str(ITEM_PER_PAGE)}
BASE_SEARCH_API_URL = "https://api.github.com/search/code"
BASE_SEARCH_URL = BASE_SEARCH_API_URL + "?" + urllib.parse.urlencode(PARAMS)

# Headers for the columns in the output CSV file
headers = ["repo_full_name", "created_at", "updated_at", "description", "num_stars",
           "num_forks", "base_language", "has_issues", "is_archived", "topics",
           "repo_languages", "size", "has_license", "num_contributors"]

def get_contributors(contributors_url, headers):
    # Function to get the number of contributors by paginating through the contributor's endpoint
    contributors_count = 0
    page = 1
    while True:
        paginated_url = f"{contributors_url}?per_page=100&page={page}"
        response = requests.get(url=paginated_url, headers=headers)
        if response.status_code == 200:
            contributors = response.json()
            contributors_count += len(contributors)
            if len(contributors) < 100:
                break
            page += 1
        else:
            handle_rate_limit(response)
    return contributors_count

def load_visited_repos(output_file):
    # Loads the set of repositories already visited to avoid duplication
    visited = set()
    try:
        with open(output_file, 'r', newline='', encoding='utf-8') as infile:
            csv_reader = csv.reader(infile)
            next(csv_reader, None)  # Skip the header
            for row in csv_reader:
                if row:
                    visited.add(row[0])
    except FileNotFoundError:
        pass
    return visited

def handle_rate_limit(response):
    # Handles API rate limiting by waiting before making new requests
    print("reponse:: ", response.headers)
    duration = int(response.headers.get("Retry-After", 60))
    logging.warning(f"Limit exhausted. Sleep for {duration} secs\n{response.text}")
    time.sleep(duration)

def get_secondary_used_languages(language_url, headers):
    # Retrieves and calculates the percentage usage of languages in the repository
    response = requests.get(url=language_url, headers=headers)
    if response.status_code == 200:
        languages = response.json()
        total_count = sum(languages.values())
        return {lang: round((count / total_count) * 100, 2) for lang, count in languages.items()}
    elif response.status_code == 403:
        handle_rate_limit(response)

def write_repo_info_to_csv(repo_info, output_file):
    # Writes the gathered repository information into a CSV file
    with open(output_file, "a", encoding='utf-8', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',')
        csv_writer.writerow(repo_info)

def setup_logging():
    # Setup logging configuration
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

def init_file(output_file, headers):
    # Initializes the CSV file and writes the header
    with open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile, delimiter=',')
        csv_writer.writerow(headers)

def main(OUTPUT_FILE):
    # The main function to orchestrate the data collection
    setup_logging()
    visited_repos = load_visited_repos(OUTPUT_FILE)
    page_index = 1
    state = True
    repos_counter = 0
    while state:
        search_url = f"{BASE_SEARCH_URL}&page={page_index}"
        headers = {"Authorization": f"token {GITHUB_API_TOKENS[page_index % len(GITHUB_API_TOKENS)]}",
                   "Accept": "application/vnd.github.v3+json"}
        g = Github(GITHUB_API_TOKENS[page_index % len(GITHUB_API_TOKENS)])
        print(g.get_rate_limit())
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            files = response.json().get("items", [])
            print('visited_repos :', visited_repos)
            for file in files:
                if file["path"].endswith(".tf"):
                    repo_full_name = file.get("repository", {}).get("full_name", None)
                    is_not_fork_repo = file.get("repository", {}).get("fork", None)
                    if is_not_fork_repo == False and repo_full_name and repo_full_name not in visited_repos:
                        repo_info = fetch_repo_info(file["repository"]["url"], headers)
                        print(repo_info)
                        if repo_info:
                            write_repo_info_to_csv(repo_info, OUTPUT_FILE)
                            visited_repos.add(repo_full_name)
                            repos_counter += 1
            page_index += 1
        elif response.status_code == 403:
            print("Please I'm waiting !!!!!!!!!!!!!!!!!!!!!!! ")  # This is the line you mentioned
            handle_rate_limit(response)
        elif response.status_code in [422, 404]:
            state = False
            logging.info(response.json().get("message", "422 or 404 Error"))
        else:
            state = False
            logging.error(f"Query failed with code {response.status_code}.\n{response.text}")
            print("!!!!! I'm Sleeping, Sorry You should wait little bit !!!!!")
            raise Exception(f"Query failed with code {response.status_code}.\n{response.text}")
            time.sleep(1800)

    logging.info(f"{repos_counter} repos added")
    print(f"{repos_counter} repos added")

def fetch_repo_info(repo_url, headers):
    # Fetches detailed information about a specific repository
    response = requests.get(url=repo_url, headers=headers)
    if response.status_code == 200:
        repo = response.json()
        repo_info = [
            repo.get("full_name"),
            repo.get("created_at"),
            repo.get("updated_at"),
            repo.get("description", ""),
            repo.get("stargazers_count", 0),
            repo.get("forks_count", 0),
            repo.get("language"),
            repo.get("has_issues", False),
            repo.get("archived", False),
            repo.get("topics", []),
            get_secondary_used_languages(f'{repo["url"]}/languages', headers),
            repo.get("size", 0),
            bool(repo.get("license")),
        ]
        return repo_info

if __name__ == '__main__':
    main(OUTPUT_FILE)
