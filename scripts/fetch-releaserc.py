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
RELEASERC_URL = f"{REPO_BASE_URL}/.releaserc.json"
RELEASERC_FILE = ".releaserc.json"

def download_releaserc():
    print(f"Downloading the .releaserc.json file from {RELEASERC_URL}")
    request = urllib.request.Request(RELEASERC_URL)
    
    try:
        with urllib.request.urlopen(request) as response, open(RELEASERC_FILE, 'wb') as out_file:
            out_file.write(response.read())
        print(f".releaserc.json file downloaded to {RELEASERC_FILE}")
    except HTTPError as e:
        print(f"Failed to download .releaserc.json file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def main():
    download_releaserc()
    print(".releaserc.json file has been set up successfully.")


if __name__ == "__main__":
    main()