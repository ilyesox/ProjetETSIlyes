import datetime
import requests
import pandas as pd
from packaging.version import parse

def fetch_versions(provider):
    # Format the URL for the specific provider
    url = f"https://registry.terraform.io/v1/providers/{provider}/versions"

    # Make a GET request to the API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        data = response.json()

        # Collect all version numbers
        versions = [version['version'] for version in data['versions']]
        versions.sort(key=parse, reverse=False)  # Sort versions in ascending order
        return versions
    except requests.RequestException as e:
        print(f"Failed to fetch versions for {provider}: {e}")
        return []

def get_provider_versions_from_csv(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Filter for rows where blockType is 'provider'
    df = df[df['blockType'] == 'provider']

    # Get unique providers from the sourceName column
    providers = df['sourceName'].unique()

    # Dictionary to hold provider versions
    provider_versions = {}

    # Loop through each provider and fetch versions
    for provider in providers:
        versions = fetch_versions(provider)
        provider_versions[provider] = versions

    return provider_versions

# Usage
csv_file = '/content/Azure__az-hop__versioning__data__1.2.2_TEST_TEST_TEST_file.csv'
versions = get_provider_versions_from_csv(csv_file)
print(versions)

def find_used_version_tilde_greater_than(declared_version, versions, provider, commit_date):
    ver = declared_version.split('.')
    missing_patch = False
    missing_minor = False
    used_version = ver[-1]
    v = '.'.join(ver[:-1])
    if used_version == '-1' :
      if ver[1] == '-1' :
        return find_used_version_greather_than(declared_version, versions, provider, commit_date)
      used_version = ver[1]
      ver = ver[0]
      missing_patch = True
    for version in versions:
        if version.startswith(v):
            if missing_patch:
                if int(used_version) >= int(version.split('.')[-2]):
                  continue
                else:
                    if get_version_date(provider, version) > commit_date:
                        break
                    used_version = int(version.split('.')[-2])
            else :
                if int(used_version) >= int(version.split('.')[-1]):
                  continue
                else:
                    if get_version_date(provider, version) > commit_date:
                        break
                    used_version = int(version.split('.')[-1])
    if(missing_patch):
      print(used_version)
      used_version = declared_version.split('.')[0]+'.'+ str(used_version)+ '.0'
    else:
      used_version = declared_version[:-1] + str(used_version)

    return used_version
!pip install packaging

from packaging import version

def find_used_version_smaller_than(declared_version, provider_versions, provider, commit_date):
  filtered_versions = [v for v in provider_versions if version.parse(v) < version.parse(declared_version) and get_version_date(provider, v) <= commit_date]
  return filtered_versions[-1]
def find_used_version_greather_than(declared_version, provider_versions, provider, commit_date):
    latest_version = None

    for version in provider_versions:
        date = get_version_date(provider, version)
        if date:
            commit_date_dt = datetime.datetime.strptime(commit_date, "%Y-%m-%d %H:%M:%S")
            version_date_dt = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            if commit_date_dt > version_date_dt:
                latest_version = version
                latest_version_date = date
            else:
                break

    return latest_version  # Ensures two values are always returned
def fetch_versions(provider):
    # Format the URL for the specific provider
    url = f"https://registry.terraform.io/v1/providers/{provider}/versions"

    # Make a GET request to the API
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for HTTP errors
        data = response.json()

        # Collect all version numbers
        versions = [version['version'] for version in data['versions']]
        versions.sort(key=parse, reverse=False)  # Sort versions in ascending order
        return versions
    except requests.RequestException as e:
        print(f"Failed to fetch versions for {provider}: {e}")
        return []

import requests
import datetime
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_version_date(provider, version):
    url = f"https://registry.terraform.io/v1/providers/{provider}/{version}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["published_at"]
    except requests.RequestException as e:
        print(f"Failed to fetch version for {provider}: {e}")
        return None

def get_latest_available_version_at_date(provider, provider_versions, commit_date):
    latest_version = None
    latest_version_date = None

    for version in provider_versions:
        date = get_version_date(provider, version)
        if date:
            commit_date_dt = datetime.datetime.strptime(commit_date, "%Y-%m-%d %H:%M:%S")
            version_date_dt = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            if commit_date_dt > version_date_dt:
                latest_version = version
                latest_version_date = date
            else:
                break

    return (latest_version, latest_version_date)  # Ensures two values are always returned
def apply_used_version(row):
    global providers_versions
    x = ''
    if(row['operator'] == '='):
      x =row['declared_version']
    elif(row['operator'] == '~>'):
      x =find_used_version_tilde_greater_than(row['declared_version'], providers_versions[row['sourceName']], row['sourceName'], row['date'])
    # elif(row['operator'] == '>='):
    #   x =find_used_version_greather_than(row['declared_version'], providers_versions[row['sourceName']], row['sourceName'], row['date'])
    # elif(row['operator'] == '<'):
    #   x =find_used_version_smaller_than(row['declared_version'], providers_versions[row['sourceName']], row['sourceName'], row['date'])

    return x

def main():
    global providers_versions
    # Load the data
    file_path = '/content/Azure__az-hop__versioning__data__1.2.2_TEST_TEST_TEST_file.csv'
    data = pd.read_csv(file_path)
    data = data[data['blockType'] == 'provider']

    # Get unique providers and fetch their versions
    providers_versions = {provider: fetch_versions(provider) for provider in data['sourceName'].unique()}

    # Apply get_latest_available_version_at_date function and expand results into two columns
    data[['latest_available_version_at_date', 'date_of_latest_available_version_at_date']] = data.apply(
        lambda row: get_latest_available_version_at_date(
            row['sourceName'],
            providers_versions[row['sourceName']],
            row['date']
        ),
        axis=1,
        result_type='expand'
    )
    data['declared_version'] = data.apply(lambda row: f"{row['major']}.{row['minor']}.{row['patch']}", axis=1)

    data['used_version'] = data.apply(lambda row : apply_used_version(row), axis=1)
    # Verify function 'get_version_date' is correctly applied to populate 'release date of used version'
    data['release date of used version'] = data.apply(
        lambda row: get_version_date(row['sourceName'], row['used_version']),
        axis=1
    )

    # Debugging: Print DataFrame columns to confirm column addition
    print("Columns after processing:", data.columns.tolist())
    print("Sample release dates:", data['release date of used version'].head())

    # Ensure columns are converted to datetime format
    data['date_of_latest_available_version_at_date'] = pd.to_datetime(data['date_of_latest_available_version_at_date'], errors='coerce')
    data['release date of used version'] = pd.to_datetime(data['release date of used version'], errors='coerce')

    # Calculate 'DELTA3'
    data['DELTA3'] = (data['date_of_latest_available_version_at_date'] - data['release date of used version']).dt.days

    # Debugging: Print sample data for DELTA3 to verify correct calculations
    print("Sample data for DELTA3:", data[['latest_available_version_at_date', 'date_of_latest_available_version_at_date', 'DELTA3']].head())

    # Save the selected columns to a CSV file
    columns_to_display = ['workingDirectory', 'sourceName', 'date', 'operator', 'declared_version', 'used_version', 'release date of used version', 'latest_available_version_at_date', 'date_of_latest_available_version_at_date', 'DELTA3']
    data[columns_to_display].to_csv('/content/tested_on_Azure__Avere.csv  ', index=False)

    # Print final DataFrame to console for verification
    print(data[columns_to_display])

if __name__ == "__main__":
    main()
