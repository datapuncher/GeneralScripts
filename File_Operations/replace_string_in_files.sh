#!/usr/bin/bash

# Usage: ./replace.sh "*.txt" "old text" "new text"

pattern="$1"
search="=$2"
replace="$3"

# Safety check
if [ $# -ne 3 ]; then
    echo "Usage: $0 \"<glob>\" \"search\" \"replace\""
    exit 1
fi

# Loop through matching files
for file in $pattern; do
    [ -e "$file" ] || continue   # skip if no match

    echo "Processing: $file"

    # GNU sed (Linux)
    sed -i "s#${search}#${replace}#g" "$file"

    # BSD sed (macOS)
    # sed -i '' "s/${search}/${replace}/g" "$file"
done

echo "Done."
