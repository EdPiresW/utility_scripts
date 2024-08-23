import io
import logging
import os
import subprocess
import sys

def get_logger(name: str, debug=False) -> logging:
    """
    Set up a logger instance and return it
    """
    new_logger = logging.getLogger(name)
    new_logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # logger itself is ensured to be a singleton
    # but handlers should only be added once
    if len(new_logger.handlers) == 0:
        console_handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S %z"
        )
        console_handler.setFormatter(formatter)
        new_logger.addHandler(console_handler)
    return new_logger

LOGGER = get_logger(__name__)

def check_remote() -> str:
    """
    Checks if the 'upstream' remote is configured and returns its URL.
    If the 'upstream' is not configured, it will ask the user to provide
    the 'upstream' URL.

    Returns:
        str: _description_
    """
    try:
        output = subprocess.check_output(["git", "remote", "-v"])
        output_str = output.decode()
        if "upstream" in output_str:
            LOGGER.info("Upstream URL: %s",output_str.split()[1].strip())
            return None
        else:
            LOGGER.warning("Upstream remote not configured. Please provide the URL.")
            upstream_url = input("Provide the upstream URL: ")
            LOGGER.info("Upstream URL: %s", upstream_url)
            return upstream_url
    except subprocess.CalledProcessError as e:
        print(f"Error checking remote: {e}")
        sys.exit(1)

def add_remote(upstream_url):
    try:
        LOGGER.info("Adding the Upstream to remote")
        subprocess.check_call(["git", "remote", "add", "upstream", upstream_url])
    except subprocess.CalledProcessError as e:
        print(f"Error adding upstream: {e}")

def git_fetch():
    try:
        LOGGER.info("Fetch changes from target branch: upstream")
        subprocess.check_call(["git", "fetch", "upstream"])
    except subprocess.CalledProcessError as e:
        print(f"Error fetching: {e}")

def git_checkout(target_branch):
    try:
        LOGGER.info("Checkout the target branch: %s", target_branch)
        subprocess.check_call(["git", "checkout", target_branch])
    except subprocess.CalledProcessError as e:
        print(f"Error checkout: {e}")

def git_rebase(target_branch):
    """Rebases the current branch."""
    try:
        LOGGER.info("Rebase the current branch on upstream/%s", target_branch)
        subprocess.check_call(["git", "rebase", f"upstream/{target_branch}"])
    except subprocess.CalledProcessError as e:
        print(f"Error rebasing: {e}")


def main():
    # Check remote branch for upstream
    if check_remote():
        add_remote(check_remote())

    # Get user input for the target branch
    target_branch = input("Target branch: ")
    git_fetch()
    git_checkout(target_branch)
    git_rebase(target_branch)



if __name__ == "__main__":
    main()
