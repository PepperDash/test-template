import os
import urllib.request
import sys
from urllib.error import HTTPError

# URL to the shared copilot-instructions.md file
COPILOT_INSTRUCTIONS_URL = "https://github.com/PepperDash/test-template/raw/main/.github/copilot-instructions.md"
COPILOT_DIR = ".github"

def create_github_directory():
    if not os.path.exists(COPILOT_DIR):
        print(f"Creating GitHub directory at {COPILOT_DIR}")
        os.makedirs(COPILOT_DIR)
    else:
        print(f"GitHub directory {COPILOT_DIR} already exists.")


def download_copilot_instructions():
    copilot_path = os.path.join(COPILOT_DIR, "copilot-instructions.md")
    print(f"Downloading the copilot instructions from {COPILOT_INSTRUCTIONS_URL}")
    request = urllib.request.Request(COPILOT_INSTRUCTIONS_URL)
    
    try:
        with urllib.request.urlopen(request) as response, open(copilot_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Copilot instructions downloaded to {copilot_path}")
    except HTTPError as e:
        print(f"Failed to download copilot instructions: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def main():
    create_github_directory()
    download_copilot_instructions()
    print("Copilot instructions have been set up successfully.")


if __name__ == "__main__":
    main()


    