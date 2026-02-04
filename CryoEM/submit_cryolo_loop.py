#!/usr/bin/env python
import shutil 
import os
import subprocess

lower_thresh=0.2
upper_thresh=0.8
thresh_incr=0.2
lower_diam=80
upper_diam=160
diam_incr=40

thresh=lower_thresh
gmodel_path='/Users/yilai/cryolo/gmodel_phosnet_20181221_loss0037.h5'
while thresh<=upper_thresh: 

	diam=lower_diam
	while diam<=upper_diam: 
	
		outdir="diam%i_thresh%.1f" %(diam,thresh)	
		
		if os.path.exists(outdir): 
			shutil.rmtree(outdir)

		os.makedirs(outdir)

		#Write out new configfile
                config_open=open('/lsi/groups/mcianfroccolab/mcianfro/aldolase/18sep26a/MotionCorr/job009/Micrographs/diam195_thresh0.30/config.json','r')
                new_config=open('config_%i_%.1f.json' %(diam,thresh),'w')
                for line in config_open:
	                if 'anchors' in line:
        	                line=line.replace('120','%.f' %(diam))
                	new_config.write(line)
                new_config.close()
                config_open.close()
	
		run_file='cryolo_submit_%i_%.1f.sh' %(diam,thresh)
                run_open=open(run_file,'w')
                cmd='#!/bin/bash\n'
                cmd+='#PBS -V\n'
                cmd+='#PBS -N Cryolo\n'
                cmd+='#PBS -k eo\n'
                cmd+='#PBS -q batch\n'
                cmd+='#PBS -l nodes=1:ppn=20\n'
                cmd+='#PBS -l walltime=72:00:00\n'
                cmd+="NSLOTS=$(wc -l $PBS_NODEFILE|awk {'print $1'})\n"
                cmd+='source /Users/mcianfro/software/modules.sh\n'
                cmd+='source activate cryolo-cluster\n'
                cmd+='module load python-anaconda3/latest \n'
                cmd+='cd $PBS_O_WORKDIR\n'
                cmd+='cryolo_predict.py -c config_%i_%.1f.json -w %s -i micrographs_subset/ -o %s/ -t %f  > %s/run.out 2> %s/run.err < /dev/null\n' %(diam,thresh,gmodel_path,outdir,thresh,outdir,outdir)

                run_open.write(cmd)
                run_open.close()

                cmd='qsub cryolo_submit_%i_%.1f.sh' %(diam,thresh)
                subprocess.Popen(cmd,shell=True)

		diam=diam+diam_incr


	thresh=thresh+thresh_incr
