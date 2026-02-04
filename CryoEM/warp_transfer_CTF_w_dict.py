#!/usr/bin/env python
import subprocess
import sys 
import os 
inwarp='goodparticles_Retrain1_BoxNet2Mask_20180531_2.star'
reformat_warp='%s_reformat_unbinned.star' %(inwarp[:-5])
if os.path.exists(reformat_warp): 
	os.remove(reformat_warp)
o2=open(reformat_warp,'w')
relionextract='Extract/job016/particles.star'
newout='%s_updatedCTF_withWarp2.star' %(relionextract[:-5])
if os.path.exists(newout): 
	os.remove(newout)
o1=open(newout,'w')
scalefactor=1.6245
microlist=[]
flipY=True
YDim=3710

'''warpmics={}
counter=0
for line in open(inwarp,'r'): 
	if len(line)<40:
		continue
	#warpmics[counter]={'micrograph':line.split()[-1][:-4]+'.mrc', 'defx':line.split()[8],}
	warpmics['micrograph']=line.split()[-1][:-4]
	counter=counter+1

print warpmics

sys.exit()
'''
for line in open(inwarp,'r'): 
	l=line.split()
	if len(line)<40:
		o2.write(line)
		continue
	warp_x=round(float(line.split()[0])*scalefactor)
        warp_y=round(float(line.split()[1])*scalefactor)
        warp_mic=line.split()[-1][:-4].replace('.frames','_frames')+'.mrc'
	if flipY is True:
        	y1=float(warp_y)
		ynew=y1-(YDim/2)
                y2=ynew*-1
                warp_y=y2+(YDim/2)
	o2.write('%.2f\t%.2f\t%s\t%s\t%s\t%s\n' %(warp_x,warp_y,l[8],l[9],l[10],l[-1][:-4].replace('.frames','_frames')+'.mrc'))
o2.close()
for line in open(relionextract,'r'): 
	if len(line)<40: 
		o1.write(line)
		continue
	relion_x=line.split()[0]
	relion_y=line.split()[1]
	micname=line.split()[2].split('/')[-1]
	
	cmd='cat %s | grep %s | grep %.2f | grep %.2f' %(reformat_warp,micname,float(relion_x),float(relion_y))
	warpinfo=subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE).stdout.read()	
	if len(warpinfo) ==0: 
		print 'error'
		print cmd
		sys.exit()
	l=line.split()
	l[10]=warpinfo.split()[2]
	l[11]=warpinfo.split()[3]
	l[12]=warpinfo.split()[4]
	o1.write('\t'.join(l)+'\n')
					



