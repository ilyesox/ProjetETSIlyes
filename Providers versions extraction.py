import pandas as pd
import requests
import json

# Load the CSV file
file_path = '/content/Azure__az-hop__versioning__data__1.2.2_TEST_TEST_TEST_file.csv'
data = pd.read_csv(file_path)

# Get unique providers from the "SourceName" column
unique_providers = data['sourceName'].unique()

# Function to fetch versions and their release dates from the Terraform Registry
def fetch_versions_and_dates(provider):
    url = f"https://registry.terraform.io/v1/providers/{provider}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            versions = response.json()["versions"]
            details = []
            for version in versions:
                version_url = f"{url}/{version}"
                version_response = requests.get(version_url)
                if version_response.status_code == 200:
                    version_data = version_response.json()
                    details.append({
                        "version": version_data["version"],
                        "published_at": version_data["published_at"]
                    })
            return details
        else:
            print(f"Failed to fetch data for {provider}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching data for {provider}: {e}")

# Loop through each provider and print their versions and release dates
for provider in unique_providers:
    print(f"\nFetching versions for {provider}")
    version_details = fetch_versions_and_dates(provider)
    if version_details:
        for detail in version_details:
            print(f"Version: {detail['version']}, Released: {detail['published_at']}")
    else:
        print(f"No details found for {provider}")

