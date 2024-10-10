import os
import urllib.request
import sys
import json
from urllib.error import HTTPError

# Load configuration from manifest file
with open("scripts/manifest.json", "r") as manifest_file:
    config = json.load(manifest_file)

REPO_BASE_URL = config.get("REPO_BASE_URL")
GITIGNORE_URL = f"{REPO_BASE_URL}/.gitignore"  # Update to point to the .gitignore file
GITIGNORE_FILE = ".gitignore"

def download_gitignore():
    print(f"Downloading the .gitignore file from {GITIGNORE_URL}")
    request = urllib.request.Request(GITIGNORE_URL)
    
    try:
        with urllib.request.urlopen(request) as response, open(GITIGNORE_FILE, 'wb') as out_file:
            out_file.write(response.read())
        print(f".gitignore file downloaded to {GITIGNORE_FILE}")
    except HTTPError as e:
        print(f"Failed to download .gitignore file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    download_gitignore()
    print(".gitignore file has been set up successfully.")

if __name__ == "__main__":
    main()