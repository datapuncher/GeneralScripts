#!/usr/bin/env python
import glob
import subprocess
import os 
import time 

inputdir='/lsi/groups/mcianfroccolab/cryoem_automation/frames/18dec13c/rawdata/'

finaldone=0
maximum=40
counter=1
while finaldone != 1: 
	#Get number of files
	nummovies1=len(glob.glob('%s/*frames.mrc' %(inputdir)))
	time.sleep(90)
	nummovies2=len(glob.glob('%s/*frames.mrc' %(inputdir)))
	if nummovies1 == nummovies2: 
		time.sleep(600)
		nummovies2=len(glob.glob('%s/*frames.mrc' %(inputdir)))
		if nummovies1 == nummovies2:
			time.sleep(600)
			nummovies2=len(glob.glob('%s/*frames.mrc' %(inputdir)))
			if nummovies1 == nummovies2:
				finaldone=1
	for movie in glob.glob('%s/*frames.mrc' %(inputdir)): 
		mrcsplit=movie.split('.')
	        del mrcsplit[-1]
		outname='%s.tif' %('.'.join(mrcsplit))
		if not os.path.exists(outname): 
			cmd='mrc2tif -s -c zip %s %s' %(movie,outname)
			print cmd 
			subprocess.Popen(cmd,shell=True).wait()
