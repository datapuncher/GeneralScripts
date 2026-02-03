#!/usr/bin/python

#import csv module
#import csv

# open and read the file into memory
#file = open('deleteHidden.txt')
#reader = csv.reader(file)

# iterate though the lines and print them
# to stdout
#for line in reader:
#   print(line)

with open("deleteHidden.txt", "r") as datafile:
  for line in datafile:   
    print line[3:51]
