#!/bin/bash

# Make a new directory to store binned images
mkdir binned_images

# Run the relion_image_handler executable for every image in
# the directory ending with *en-a.mrc
for file in ./*en-a.mrc
do
   relion_image_handler --rescale_angpix 4.0 --i $file --o binned_images/$file
done
