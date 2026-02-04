#!/usr/bin/env python
import os 
import sys
import time
import subprocess
import glob

indir='/lsi/cryoem_automation/frames/17nov27a/rawdata/'
tot=len(glob.glob('Micrographs/*frames.mrc'))
#ext='nov27a_prex_00035gr_00069sq_v02_00009hl_00005en.frames.mrc'
ext='frames.mrc' #frames.mrc'
ref1='/lsi/cryoem_automation/frames/17nov27a/rawdata/references/17nov27a_27135059_01_7420x7676_norm_0.mrc'
ref2='/lsi/cryoem_automation/frames/17nov27a/rawdata/references/17nov27a_30101009_01_7420x7676_norm_0.mrc'
isdone=0
maxgpus=4
while isdone == 0: 

	#time.sleep(60)
	numfiles=len(glob.glob('%s/*frames.mrc' %(indir)))

	if numfiles == tot: 
		time.sleep(300)
		numfiles=len(glob.glob('%s/*frames.mrc' %(indir)))
		if numfiles == tot:
                	time.sleep(300)
                	numfiles=len(glob.glob('%s/*frames.mrc' %(indir)))	
			if numfiles == tot: 
				isdone=1

	if numfiles != tot: 

		#Create list of done mics
		frameslist=[]
		frameslistin=glob.glob('/lsi/cryoem_automation/frames/17nov27a/rawdata/*frames.mrc')
		for frame in frameslistin: 
			if not os.path.exists('Micrographs/%s' %(frame.split('/')[-1])): 
				frameslist.append(frame)
		counter=0
		while counter < len(frameslist): 

			monitordone=[]
			gpucounter=0
			while gpucounter<maxgpus: 
				createddate=time.strftime('%d', time.gmtime(os.path.getmtime(frameslist[counter])))
				
				if float(createddate) < 30: 
					referenceimage=ref1
				if float(createddate) >= 30: 
					referenceimage=ref2
			
				cmd='MotionCor2 -InMrc %s -OutMrc Micrographs/%s -Gain %s -Patch 5 5 -Gpu %i -FtBin 2' %(frameslist[counter],frameslist[counter].split('/')[-1],referenceimage,gpucounter)
				print cmd
				subprocess.Popen(cmd,shell=True)
				
				monitordone.append('Micrographs/%s' %(frameslist[counter].split('/')[-1]))

				counter=counter+1
				if counter>= len(frameslist): 
					counter=len(frameslist)
					gpucounter=5
				gpucounter=gpucounter+1
	
			print monitordone			
			#Wait
			isbatchdone=0
			while isbatchdone != maxgpus: 
				for checkmic in monitordone:
					if os.path.exists(checkmic) is True: 
						isbatchdone=isbatchdone+1
					
			print 'finished with first four'
			sys.exit()	

	
