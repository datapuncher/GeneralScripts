#!/usr/bin/env python
import sys
import subprocess
import os
micstar='CtfFind/job002/micrographs_ctf_sel_res6_df13_50.star'
newmic='%s_noGoldCorner.star' %(micstar[:-5])
o1=open(newmic,'w')
boxfile='Micrographs/box_check/Micrographs/17sep27a_grid4_00029gr_00064sq_v02_00015hl_00001ed.frames.box'

#Copy to match all other names
for line in open(micstar,'r'): 

	if len(line) < 40:
		o1.write(line) 
		continue

	mic=line.split()[0].strip()

	if os.path.exists('corners.img'): 
		os.remove('corners.img')
	if os.path.exists('corners.hed'): 
		os.remove('corners.hed') 

	cmd='batchboxer input=%s dbbox=%s output=corners.img ' %(mic,boxfile)
	subprocess.Popen(cmd,shell=True).wait()	

	iminfo0=float(subprocess.Popen('e2iminfo.py corners.img -N 0 -s',shell=True, stdout=subprocess.PIPE).stdout.read().strip().split()[15].split('=')[-1])
	iminfo1=float(subprocess.Popen('e2iminfo.py corners.img -N 1 -s',shell=True, stdout=subprocess.PIPE).stdout.read().strip().split()[15].split('=')[-1])
	iminfo2=float(subprocess.Popen('e2iminfo.py corners.img -N 2 -s',shell=True, stdout=subprocess.PIPE).stdout.read().strip().split()[15].split('=')[-1])
	iminfo3=float(subprocess.Popen('e2iminfo.py corners.img -N 3 -s',shell=True, stdout=subprocess.PIPE).stdout.read().strip().split()[15].split('=')[-1])

	if iminfo0 >15: 
		if iminfo1>15: 
			if iminfo2>15: 
				if iminfo3>15: 
					o1.write(line)
		
