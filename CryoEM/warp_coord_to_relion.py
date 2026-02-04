#!/usr/bin/env python
import glob 
import os
import subprocess
import sys 

warpindir='matching'
outdir='movies'
multiplier_for_coord=1.6249
extension_to_remove='_BoxNet2_20180602.star'
flipY=True 
Ydim=3710

for boxfile in glob.glob("%s/*.star"%(warpindir)): 
	newbox='%s/%s.star' %(outdir,boxfile.split('/')[-1][:-len(extension_to_remove)])
	newbox=newbox.replace('.frames','_frames')	
	if os.path.exists(newbox): 
		os.remove(newbox)
	o1=open(newbox,'w')
	for line in open(boxfile,'r'): 
		if len(line)<40: 
			o1.write(line)
			continue
		l=line.split()
		l[0]=str(round(float(l[0])*multiplier_for_coord))[:-2]
		l[1]=str(round(float(l[1])*multiplier_for_coord))[:-2]
		l[2]=outdir+'/'+l[2].replace('.frames','_frames')
		if flipY is True: 
                        y1=float(l[1])
                        ynew=y1-(Ydim/2)
                        y2=ynew*-1
                        y2=y2+(Ydim/2)
                        l[1]=str(y2)
		line='\t'.join(l)
		o1.write(line+'\n')

	o1.close()
