#!/usr/bin/bash

# Define variables for file type, search string, and replacement string
FILE_TYPE="star"
SEARCH_STRING="extract"
REPLACEMENT_STRING="extracted"

# Check if the required arguments are provided
if [ -z "$FILE_TYPE" ] || [ -z "$SEARCH_STRING" ] || [ -z "$REPLACEMENT_STRING" ]; then
    echo "Usage: $0 <file_type> <search_string> <replacement_string>"
    echo "Example: $0 txt \"old text\" \"new text\""
    exit 1
fi

# Find files of the specified type and perform the replacement
find . -type f -name "*.$FILE_TYPE" -exec sed -i "s/$SEARCH_STRING/$REPLACEMENT_STRING/g" {} \;

echo "Replacement complete for files of type *.$FILE_TYPE."
