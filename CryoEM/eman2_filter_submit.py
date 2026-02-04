#!/usr/bin/env python
import shutil 
import sys
import glob
import subprocess
import time
import os 

indir='/lsi/groups/mcianfroccolab/mcianfro/prex/18sep06b/relion_motioncor2/Micrographs/'
inmiclist=glob.glob("%s/*.mrc" %(indir))
counter=1
for mic in inmiclist: 
	print mic
	if os.path.exists(mic):
	        outfile='submit_%i.sh' %(int(time.time()))
	        o1=open(outfile,'w')
        	o1.write('#!/bin/bash\n')
	        o1.write('#PBS -V\n')
        	o1.write('#PBS -N eman2_filter\n')
	        o1.write('#PBS -k eo\n')
        	o1.write('#PBS -q batch\n')
	        o1.write('#PBS -l nodes=1:ppn=1\n')
        	o1.write('#PBS -l walltime=1:00:00\n')
	        o1.write('NSLOTS=$(wc -l $PBS_NODEFILE|awk {"print $1"})\n')
        	o1.write('source /Users/mcianfro/software/modules.sh\n')
        	o1.write('cd $PBS_O_WORKDIR\n')
		o1.write('module load eman2 && e2proc2d.py --process=filter.lowpass.gauss:cutoff_freq=0.1 %s Micrographs_filtered/%s\n' %(mic,mic.split('/')[-1]))

	        cmd='qsub %s' %(outfile)
		subprocess.Popen(cmd,shell=True)

		if counter % 200 == 0: 
			time.sleep(90)

		counter=counter+1
