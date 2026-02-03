#!/bin/bash

#Recursively search all subdirectories and
#make a list of files matching a pattern:

find . -mindepth 3 -type f -iname *frames.mrc > framesCount.txt
 
#Write list lines in framesCount.txt matching
#the pattern frames.mrc:

grep frames.mrc framesCount.txt > framesTotal.txt

#Get a count of lines in framesCount.txt matching
#the pattern frames.mrc:

grep frames.mrc framesCount.txt | wc -l

#Get a count of the number of mrc movie
#files in the frames/rawdata directories:

grep rawdata framesTotal.txt | wc -l
