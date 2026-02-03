#!/usr/bin/python

# Copy micrographs to the data locker while preserving symlinks and metadata
# Invoke script from your project directory

import shutil

source = "Micrographs/*.mrc"
destination "/lsi/locker/mohilab/22sept23a/Micrographs"

try:
    # Check that destination directory exists
    os.makedirs(destination, exist_ok=True)

    # Copy the source to the destination
    shutil.copy2(source, destination)
    print(f"File '{source}' copied successfully to '{destination}'")

except FileNotFoundError:
    print(f"Error: Source file '{source}' not found.")
except PermissionError:
    print(f"Error: Permission denied when trying to copy to '{destination}'.")
except Exception as e:
    print(f"An exception error occurred: {e}")
