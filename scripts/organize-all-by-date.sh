#!/bin/bash

# Organize files by date in all subdirectories
# Loops through each subdirectory and calls organize-by-date.sh

SCRIPT_DIR="$(dirname "$0")"
TARGET_DIR="${1:-.}"

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory not found: $TARGET_DIR"
    exit 1
fi

for subdir in "$TARGET_DIR"/*/; do
    # Skip if no subdirectories exist
    [[ ! -d "$subdir" ]] && continue

    echo "=== Processing: $subdir ==="
    "$SCRIPT_DIR/organize-by-date.sh" "$subdir"
done

echo "=== Done ==="
