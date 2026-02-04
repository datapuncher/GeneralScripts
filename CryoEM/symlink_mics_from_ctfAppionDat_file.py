#!/usr/bin/env python

import os 
import sys 

if len(sys.argv) < 3: 
	print " Usage: symlink_mics_from_ctfAppionDat_file.py [file from appion].dat [destination dir full path]"
	print "\n $ /Users/mcianfro/software/repo/mike_homemade_lib/symlink_mics_from_ctfAppionDat_file.py ctf-session00019.dat /Users/mcianfro/files/Micrographs"
	sys.exit()

inputfile=sys.argv[1]
outdir=sys.argv[2]

if not os.path.exists(sys.argv[2]): 
	print 'Error: destination directory does not exist. Exiting'
	sys.exit()


for line in open(inputfile,'r'): 

	if 'nominal_def' in line: 
		continue

	micname=line.split()[14]
	session=micname.split('_')[0]

	sessionpath='/lsi/cryoem_automation/leginon/%s/rawdata/' %(session)

	if not os.path.exists('%s/%s.mrc' %(sessionpath,micname)): 
		print 'Could not find %s/%s.mrc' %(sessionpath,micname)
		continue

	os.symlink('%s/%s.mrc' %(sessionpath,micname),'%s/%s.mrc' %(outdir,micname))


