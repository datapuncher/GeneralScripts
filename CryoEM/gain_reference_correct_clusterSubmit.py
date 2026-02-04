#!/usr/bin/env python
import sys 
import time 
import glob
import subprocess

gainreference='17sep25a_25151726_05_3710x3838_norm_0_mod.mrc'
inmoviedir='/lsi/groups/mcianfroccolab/mcianfro/PKA/17sep27a/18feb22z_stack1/movies'
outmoviedir='/lsi/groups/mcianfroccolab/mcianfro/PKA/17sep27a/18feb22z_stack1/movies_gain_corrected'

counter=1

for inmovie in glob.glob('%s/*_movie.mrcs' %(inmoviedir)): 

	cmd='clip mult -m 2 %s %s %s/%s' %(inmovie,gainreference,outmoviedir,inmovie.split('/')[-1])

	outfile='submit_%i.sh' %(int(time.time()))
	o1=open(outfile,'w')
	o1.write('#!/bin/bash\n')
	o1.write('#PBS -V\n')
	o1.write('#PBS -N imod_gain_correct\n')
	o1.write('#PBS -k eo\n')
	o1.write('#PBS -q batch\n')
	o1.write('#PBS -l nodes=1:ppn=1\n')
	o1.write('#PBS -l walltime=3:00:00\n')
	o1.write('NSLOTS=$(wc -l $PBS_NODEFILE|awk {"print $1"})\n')
	o1.write('source /Users/mcianfro/software/modules.sh\n')
	o1.write('module load imod\n')
	o1.write('cd $PBS_O_WORKDIR\n')
	o1.write('%s\n' %(cmd))
	o1.close()

	cmd='qsub %s' %(outfile)
	subprocess.Popen(cmd,shell=True).wait()

	if counter%20 == 0: 
		time.sleep(360)

	counter=counter+1
