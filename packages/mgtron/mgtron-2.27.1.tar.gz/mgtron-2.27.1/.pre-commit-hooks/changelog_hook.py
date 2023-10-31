#!/usr/bin/env python3

import subprocess


def main():
    """Script that copies the changelog from the main
    directory to src/assets/Changelog.cpy"""

    # Copy the changelog from the main directory to src/assets/Changelog.cpy
    command = "cp CHANGELOG.md src/assets/CHANGELOG.cpy"

    # Run the command
    subprocess.run(command, shell=True)

    # Add the file to the staging area
    command = "git add src/assets/CHANGELOG.cpy"

    # Run the command
    subprocess.run(command, shell=True)

    # Exit the script
    exit(0)


if __name__ == "__main__":
    main()
