#!/bin/bash

# Make directory to hold binned images
mkdir binned_images

# Iterate over all *en-a.mrc and run EMAN2 command to bin them
for file in ./*en-a.mrc
do
   e2proc2d.py $file binned_images/$file --meanshrink=4
done
