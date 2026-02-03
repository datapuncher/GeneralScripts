#!/usr/bin/python

# Open density map in binary mode for read only. Used with the 'mrcfile' I/O library 
with open('apoferritin.mrc', 'rb') as f:
   byte=f.read(1)
   while byte != "":
      byte=f.read(1) 
