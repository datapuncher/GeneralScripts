#!/bin/bash

# Delete all files in current directory that are not listed 
# in the input text file

cat corrected_micrographs.star | awk '{print $1}' | sed -n '11,$p' | xargs rm -rf
