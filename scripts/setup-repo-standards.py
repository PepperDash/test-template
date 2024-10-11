import subprocess
import sys

def switch_branch():
    suggested_branch = "set-repo-standards"
    current_branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
    
    print(f"Current branch is '{current_branch}'.")
    user_input = input(f"Would you like to switch to a different branch? (y to switch / n to stay): ").strip().lower()

    if user_input == 'y':
        branch_name = input(f"Enter the branch name to switch to (default: '{suggested_branch}'): ").strip() or suggested_branch
        print(f"Switching to branch '{branch_name}'. If it doesn't exist, it will be created.")
        try:
            # Try to check out the branch, or create it if it doesn't exist
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        except subprocess.CalledProcessError:
            # If branch already exists, just check it out
            subprocess.run(["git", "checkout", branch_name], check=True)
    else:
        print(f"Staying on the current branch '{current_branch}'.")

def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        subprocess.run(["python", f"scripts/{script_name}.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {script_name}: {e}")
        # Instead of exiting, we log the error and continue
        return False
    return True

def main():
    # Step 1: Prompt to switch to the suggested branch
    switch_branch()

    # Step 2: Run each script to set up the standards
    scripts = [
        "fetch-copilot-instructions",
        "fetch-gitattributes",
        "fetch-gitignore",
        "fetch-releaserc",
        "setup-hooks"
    ]

    all_passed = True
    for script in scripts:
        success = run_script(script)
        if not success:
            all_passed = False

    if all_passed:
        print("Repository standards have been set up successfully.")
    else:
        print("Some scripts failed. Please check the logs above for more details.")


if __name__ == "__main__":
    main()