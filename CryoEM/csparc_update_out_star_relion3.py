#!/usr/bin/env python

#This will update a csparc2star output star file into the original extract particle stack so that bayesian polishing will work
#This will create a new file that 'only' as the particles found the csparc file

import os
import sys

csparc='cryosparc_exp000656_003.star'
csparc_part_colnum=11
extract='Extract/job032/particles_update.star'
extract_part_colnum=3
newextract='Extract/job032/particles_csparc_sel.star'

if os.path.exists(newextract): 
	print 'error output %s already exists. exiting' %(newextract)
	sys.exit()

csparclist=[]

for line in open(csparc,'r'): 
	if len(line)<40: 
		continue
	rlnimage=line.split()[csparc_part_colnum-1]
	if rlnimage not in csparclist: 
		csparclist.append(rlnimage)
o1=open(newextract,'w')
for line in open(extract,'r'): 
	if len(line)<40: 
		o1.write(line)
		continue
	rlnimage=line.split()[extract_part_colnum-1]
	if rlnimage in csparclist: 
		o1.write(line)


