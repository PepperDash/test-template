import os
import sys
import subprocess

HOOKS_DIR = ".githooks"
HOOK_FILE = "commit-msg"

def remove_commit_msg_hook():
    hook_path = os.path.join(HOOKS_DIR, HOOK_FILE)
    if os.path.exists(hook_path):
        try:
            os.remove(hook_path)
            print(f"Removed commit message hook at {hook_path}")
        except Exception as e:
            print(f"Failed to remove commit message hook: {e}")
            sys.exit(1)
    else:
        print(f"No commit message hook found at {hook_path}, nothing to remove.")


def reset_git_hooks_path():
    print("Resetting Git hooks path to default.")
    try:
        subprocess.run(["git", "config", "--unset", "core.hooksPath"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to reset Git hooks path: {e}")
        sys.exit(1)

def main():
    remove_commit_msg_hook()
    reset_git_hooks_path()
    print("Commit message hook enforcement has been stopped successfully.")


if __name__ == "__main__":
    main()