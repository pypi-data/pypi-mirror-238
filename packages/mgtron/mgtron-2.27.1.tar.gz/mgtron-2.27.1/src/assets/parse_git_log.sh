#!/bin/bash

set -e

output_file="./output.txt"

touch $output_file

# Define the list of keywords to filter
keywords=("fix" "wip" "feat" "chore" "doc")

echo "Parsing git log..."

# Parse git log and extract commit messages
git log --pretty=format:"%s" | while IFS= read -r line; do
    # Check if the commit message contains any of the specified keywords and a colon
    for keyword in "${keywords[@]}"; do
        if [[ $line == *"$keyword"*":"* ]]; then
	    # Only keep one of each keyword found
	    if ! grep -q "$keyword" "$output_file"; then
		echo "$line" >> "$output_file"
	    fi
	fi
    done
done


