#!/usr/bin/python

with open('emd_4274.map', 'rb') as f:
   byte=f.read(1)
   while byte != "":
      byte=f.read(1) 
