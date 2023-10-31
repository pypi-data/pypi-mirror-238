#!/bin/bash

# Assuming your CHANGELOG file is named "CHANGELOG.md"
changelog_file="CHANGELOG.md"

# Check if the CHANGELOG file exists
if [ ! -f "$changelog_file" ]; then
  echo "Could not find $changelog_file"
  exit 1
fi

# Find the latest version number using a regular expression
latest_version=$(grep -Eo '\[[0-9]+\.[0-9]+\.[0-9]+\]' "$changelog_file" | head -n 1 | tr -d '[]')

echo "$latest_version"
