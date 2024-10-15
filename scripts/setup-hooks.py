import os
import subprocess
import urllib.request
import sys
import json
import hashlib
from urllib.error import HTTPError

# Load configuration from manifest file
try:
    with open("scripts/manifest.json", "r") as manifest_file:
        config = json.load(manifest_file)
except FileNotFoundError:
    print("Error: manifest.json file not found in the scripts directory.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: manifest.json is not a valid JSON file.")
    sys.exit(1)

REPO_BASE_URL = config.get("REPO_BASE_URL")
BRANCH = config.get("BRANCH")
HOOKS_REPO_URL = f"{REPO_BASE_URL}/.githooks/commit-msg"
HOOKS_DIR = ".git/hooks"


def create_hooks_directory():
    if not os.path.exists(HOOKS_DIR):
        print(f"Creating hooks directory at {HOOKS_DIR}")
        os.makedirs(HOOKS_DIR)
    else:
        print(f"Hooks directory {HOOKS_DIR} already exists.")


def download_hook():
    hook_path = os.path.join(HOOKS_DIR, "commit-msg")
    print(f"Downloading the latest hook from {HOOKS_REPO_URL}")
    request = urllib.request.Request(HOOKS_REPO_URL)
    
    try:
        with urllib.request.urlopen(request) as response:
            new_hook_content = response.read()
            if os.path.exists(hook_path):
                with open(hook_path, 'rb') as existing_file:
                    existing_hook_content = existing_file.read()
                # Compare hashes to determine if download is needed
                if hashlib.sha256(existing_hook_content).hexdigest() == hashlib.sha256(new_hook_content).hexdigest():
                    print("Hook is already up to date. Skipping download.")
                    return
            # Write new hook content
            with open(hook_path, 'wb') as out_file:
                out_file.write(new_hook_content)
            print(f"Hook downloaded to {hook_path}")
    except HTTPError as e:
        print(f"Failed to download hook: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def make_hook_executable():
    hook_path = os.path.join(HOOKS_DIR, "commit-msg")
    if os.name == 'posix':  # For Unix-like systems
        print(f"Making the hook executable.")
        try:
            subprocess.run(["chmod", "+x", hook_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to make hook executable: {e}")
            sys.exit(1)
    else:
        print("Skipping chmod on Windows.")


def configure_git_hooks_path():
    print("Configuring Git to use the hooks directory.")
    try:
        subprocess.run(["git", "config", "core.hooksPath", HOOKS_DIR], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to configure Git hooks path: {e}")
        sys.exit(1)


def verify_commit_msg_hook():
    hook_path = os.path.join(HOOKS_DIR, "commit-msg")
    print("Verifying that the commit-msg hook exists.")
    if not os.path.exists(hook_path):
        print(f"Error: commit-msg hook not found at {hook_path}")
        sys.exit(1)
    print("Commit-msg hook verification passed.")


def main():
    create_hooks_directory()
    download_hook()
    make_hook_executable()
    configure_git_hooks_path()
    verify_commit_msg_hook()
    print("Git hooks have been set up successfully.")


if __name__ == "__main__":
    main()