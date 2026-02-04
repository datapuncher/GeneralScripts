#!/usr/bin/env python

import glob
import os 
import subprocess 

indir='micrographs_filtered'
miclist=glob.glob('%s/*.mrc' %(indir))
for mic in miclist: 
	cmd=float(subprocess.Popen('header %s | grep Number' %(mic),shell=True, stdout=subprocess.PIPE).stdout.read().strip().split()[-1])	
	if cmd != 1.0: 
		os.remove(mic)
		print mic
