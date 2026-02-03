#!/usr/bin/python

import os, shutil

# Initialize an empty listt for files and a counter for folder names
lis = []
i = 1

# Define the destination folder path
destinationdir = '/Users/porta031/Downloads/Moved'

# Check if the folder already exists and create a unique name if needed
while os.path.exists(destinationdir):
    destinationdir += str(i)
    i += 1

os.makedirs(destinationdir)

# List all files on the desktop
lis = os.listdir('/Users/porta031/Downloads')

# Loop through files and move them to the destination folder
for x in lis:
    print(x)
    if x == __file__:  # Skip the script file itself
        continue
    shutil.move(x, destinationdir)
