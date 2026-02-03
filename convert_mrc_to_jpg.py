#!/usr/bin/python

import glob
import os
import subprocess

# Define which frames are to be converted to jpg
infiles='/lsi/groups/mohilab/jporta/merge_18jan18c_18aug03b_reprocess/MotionCorr/job027/18jan18c/*frames.mrc'

# Iterate over the mrc files and batch convert them by invoking script
for mic in glob.glob(infiles):
    cmd='qsub -v INFILE="%s",OUTFILE="%s" /Users/jporta/software/repo/lib/convert_mrc_to_jpg_submit.sh' %(mic,mic[:-4]+'.jpg')
    subprocess.Popen(cmd,shell=True).wait()	 
	
