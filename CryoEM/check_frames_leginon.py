#!/usr/bin/env python

leginondir='/lsi/groups/mcianfroccolab/cryoem_automation/leginon/'
framesdir='/lsi/groups/mcianfroccolab/cryoem_automation/frames/'

import glob
matched=0
doesnt=0
for folders in glob.glob('%s/*' %(framesdir)): 
	session=folders.split('/')[-1]
	leginon='%s/%s/rawdata' %(leginondir,session)
	num_files_leginon=len(glob.glob('%s/*en.mrc' %(leginon)))
	num_files_frames=len(glob.glob('%s/rawdata/*frames.mrc' %(folders)))
	num_files_frames_tif=len(glob.glob('%s/rawdata/*frames.tif' %(folders)))
	if num_files_frames_tif>num_files_frames: 
		num_files_frames=num_files_frames_tif
	#if num_files_leginon>50: 
	if num_files_leginon==num_files_frames:
		#print session+'leginon: %i'%num_files_leginon+'frames:%i'%num_files_frames
		matched=matched+1
	if num_files_leginon!=num_files_frames:
                #print session+'leginon: %i'%num_files_leginon+'frames:%i'%num_files_frames
                doesnt=doesnt+1
		if num_files_leginon>50: 
			print folders
	
print doesnt
print matched	
