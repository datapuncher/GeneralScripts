#!/usr/bin/env python
import os

infile='goodparticles_Retrain1_BoxNet2Mask_20180531_2.star'
outdir='movies'
multiplier_for_coord=1.6249
extension_to_remove='_BoxNet2_20180602.star'
flipY=True
Ydim=3710

#Get micros
microlist=[]
for line in open(infile,'r'): 
	if len(line)<40:
		continue
	if line.split()[-1] not in microlist: 
		microlist.append(line.split()[-1])

#create new starfiles
for micro in microlist: 
	newstar='%s/%s.star' %(outdir,micro.replace('.frames','_frames')[:-4])
        if os.path.exists(newstar):
	        os.remove(newstar)
        newopen=open(newstar,'w')
        newopen.write('data_\n')
        newopen.write('loop_\n')
        newopen.write('_rlnCoordinateX #1\n')
        newopen.write('_rlnCoordinateY #2\n')
        newopen.write('_rlnMicrographName #3\n')
        newopen.write('_rlnAutopickFigureOfMerit #4\n')
	star=open(infile,'r')
	for line in star: 
		if len(line)>40: 
			if line.split()[-1] == micro: 
				l=line.split()
		                l[0]=str(round(float(l[0])*multiplier_for_coord))[:-2]
		                l[1]=str(round(float(l[1])*multiplier_for_coord))[:-2]
		                if flipY is True:
                		        y1=float(l[1])
		                        ynew=y1-(Ydim/2)
                		        y2=ynew*-1
		                        y2=y2+(Ydim/2)
                		        l[1]=str(y2)
				newopen.write('%s\t%s\t%s\t0.9\n' %(l[0],l[1],micro))	
	newopen.close()
	star.close()

