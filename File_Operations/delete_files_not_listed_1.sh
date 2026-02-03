#!/bin/bash

###Delete all files in current directory###
###that are not listed in text file###

#find . -name "*.star" | grep -vFf starfiles.txt | xargs rm -rf

cat corrected_micrographs.star | awk '{print $1}' | sed -n '11,$p' | xargs rm -rf
