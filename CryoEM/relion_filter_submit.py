#!/usr/bin/env python
import shutil 
import sys
import glob
import subprocess
import time
import os 

indir='/lsi/groups/mcianfroccolab/mcianfro/aldolase/18oct17a/Micrographs'

if os.path.exists('%s/mics_filtered' %(indir)): 
	print 'error out dir exists'
	sys.exit()
os.makedirs('%s/mics_filtered' %(indir))
outdir='%s/mics_filtered' %(indir)
angpix=0.91 
inmiclist=glob.glob("%s/*.mrc" %(indir))
counter=1
for mic in inmiclist: 
	if os.path.exists(mic):
	        outfile='submit_%i.sh' %(int(time.time()))
	        o1=open(outfile,'w')
        	o1.write('#!/bin/bash\n')
	        o1.write('#PBS -V\n')
        	o1.write('#PBS -N relion_filter\n')
	        o1.write('#PBS -k eo\n')
        	o1.write('#PBS -q batch\n')
	        o1.write('#PBS -l nodes=1:ppn=1\n')
        	o1.write('#PBS -l walltime=1:00:00\n')
	        o1.write('NSLOTS=$(wc -l $PBS_NODEFILE|awk {"print $1"})\n')
        	o1.write('source /Users/mcianfro/software/modules.sh\n')
        	o1.write('cd $PBS_O_WORKDIR\n')
		o1.write('module load relion && relion_image_handler --i %s --o %s/%s --angpix %f --lowpass 10\n' %(mic,outdir,mic.split('/')[-1],angpix))
		o1.close()

	        cmd='qsub %s' %(outfile)
		subprocess.Popen(cmd,shell=True)

		time.sleep(1)
		if counter % 200 == 0: 
			time.sleep(60)

		counter=counter+1
