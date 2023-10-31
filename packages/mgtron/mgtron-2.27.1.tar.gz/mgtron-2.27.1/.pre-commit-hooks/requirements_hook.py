#!/usr/bin/env python3

import subprocess


def main():
    """Script that pip freezes the requirements.txt file"""

    # Pip freeze the requirements.txt file
    command = "./venv/bin/pip freeze > requirements.txt"

    # Run the command
    subprocess.run(command, shell=True)

    # Add the file to the staging area
    command = "git add requirements.txt"

    # Run the command
    subprocess.run(command, shell=True)

    # Exit the script
    exit(0)


if __name__ == "__main__":
    main()
