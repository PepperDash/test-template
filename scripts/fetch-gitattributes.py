import os
import urllib.request
import sys
import json
from urllib.error import HTTPError

# Load configuration from manifest file
with open("scripts/manifest.json", "r") as manifest_file:
    config = json.load(manifest_file)

REPO_BASE_URL = config.get("REPO_BASE_URL")
BRANCH = config.get("BRANCH")
GITATTRIBUTES_URL = f"{REPO_BASE_URL}/.gitattributes"
GITATTRIBUTES_FILE = ".gitattributes"

def download_gitattributes():
    print(f"Downloading the .gitattributes file from {GITATTRIBUTES_URL}")
    request = urllib.request.Request(GITATTRIBUTES_URL)
    
    try:
        with urllib.request.urlopen(request) as response, open(GITATTRIBUTES_FILE, 'wb') as out_file:
            out_file.write(response.read())
        print(f".gitattributes file downloaded to {GITATTRIBUTES_FILE}")
    except HTTPError as e:
        print(f"Failed to download .gitattributes file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def main():
    download_gitattributes()
    print(".gitattributes file has been set up successfully.")


if __name__ == "__main__":
    main()