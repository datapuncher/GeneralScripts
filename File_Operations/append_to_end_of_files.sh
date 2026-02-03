#!/bin/bash

# Specify the directory to search in
directory="./"

# Specify the file type
file_type="txt"

# Specify the characters to append
characters="_appended"

# Loop through all files of the specified type in the directory
for file in "$directory"/*."$file_type"; do
  # Append the characters to the file
  echo "$characters" >> "$file"
done
