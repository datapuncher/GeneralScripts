#!/usr/bin/env python

# How to use: 
# 1. Copy into working directory
# 2. Edit to include correct file names
# 3. Run: ./create_go_ctf_input_for_warp.py

# Input information needed
inputfile='goodparticles_Retrain1_BoxNet2Mask_20180531_2.star'

# Average images from warp directory
indirectory='average'

# Script starts here
# Import python librarys
import glob
import os

# Get list of micrographs
inputmiclist=glob.glob('%s/*.mrc' %(indirectory))

# Loop over all micrographs to check if output go.star exists and then write out go.star files 
for mic in inputmiclist: 

	# Print info
	print 'working on %s' %(mic)

	# Check if output go.star exists: 
	if os.path.exists('%s_go.star' %(mic[:-5])): 
		print '--->Output file %s_go.star exists. Skipping' %(mic[:-5])

	onlymicname=mic.split('/')[-1]
	onlymicnameTIF='%s.tif' %(onlymicname[:-4])

	# Name new output file
	newout='%s_go.star' %(mic[:-4])

	# Open output file for writing 	
	o1=open(newout,'w')

	# Open warp star file
	warpopen=open(inputfile,'r')
	for line in warpopen: 
		
		# Write headers to new file if len is less than 40 characters
		if len(line)<40: 
			o1.write(line)
			continue
		# Check if micname is in line. If so, write to output
		if onlymicnameTIF in line: 
			o1.write(line)

	# Close warp star file
	warpopen.close()

	# Close output file newout
	o1.close()
