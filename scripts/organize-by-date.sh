#!/bin/bash

# Organize files by ISO date prefix
# Moves files starting with "2025-" into subdirectories named after the date (e.g., 2025-10-17/)

TARGET_DIR="${1:-.}"

cd "$TARGET_DIR" || exit 1

for file in 2025-*; do
    # Skip if no matches or if it's a directory
    [[ ! -f "$file" ]] && continue

    # Extract the ISO date (first 10 characters)
    ISO_DATE="${file:0:10}"

    # Create subdirectory if it doesn't exist
    mkdir -p "$ISO_DATE"

    # Move the file into the subdirectory
    mv "$file" "$ISO_DATE/"
    echo "Moved: $file -> $ISO_DATE/"
done
