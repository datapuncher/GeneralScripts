#!/usr/bin/python

#This script will take an input directory and compress all movies into TIFF, removing .mrc files
import time
import sys
import glob
import os
import subprocess

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

if len(sys.argv)!=2:
        print('\nThis script will take an input directory and compress all movies into TIFF, removing .mrc files \n')
	print('\nTo use: ./compress_directory_MRC_to_TIFF.py [full path to directory name]\n')
        sys.exit()

indirectory=sys.argv[1]

# Check directory exists
if not os.path.exists(indirectory):
	print('Error: Input directory does not exist %s' %(indirectory))
	sys.exit()

# Check how many mrc and tif files there are
numTIFF=len(glob.glob('%s/*.tif' %(indirectory)))
numMRC=len(glob.glob('%s/*.mrc' %(indirectory)))

if numTIFF >0:
	ans=query_yes_no("\nFound %i .tif and %i .mrc files within input directory %s \n\nDo you want to continue?" %(numTIFF,numMRC,indirectory))
	if ans is False:
		sys.exit()

ans=query_yes_no("\nFound %i movies with .mrc extension %s\n\nDo you want to compress .mrc files?" %(numMRC,indirectory))

if ans is True:
	print('\nCompressing files by submitting to the cluster...')

	delans=query_yes_no("\nDelete MRC files after compression?\n")
	counter=1
	for mrc in glob.glob('%s/*.mrc' %(indirectory)):

		mrcsplit=mrc.split('.')
		del mrcsplit[-1]
		outname='%s.tif' %('.'.join(mrcsplit))
		if not os.path.exists(outname):
			cmd='mrc2tif -s -c zip %s %s' %(mrc,outname)
			if delans is True:
				cmd=cmd+'\n'+'rm %s' %(mrc)
		        outfile='submit_%i.sh' %(int(time.time()))
        		o1=open(outfile,'w')
		        o1.write('#!/bin/bash\n')
        		o1.write('#PBS -V\n')
		        o1.write('#PBS -N mrc2tif\n')
	        	o1.write('#PBS -k eo\n')
		        o1.write('#PBS -q batch\n')
        		o1.write('#PBS -l nodes=1:ppn=1\n')
		        o1.write('#PBS -l walltime=0:60:00\n')
        		o1.write('NSLOTS=$(wc -l $PBS_NODEFILE|awk {"print $1"})\n')
	        	o1.write('source /Users/mcianfro/software/modules.sh\n')
	        	o1.write('module load imod\n')
		        o1.write('cd $PBS_O_WORKDIR\n')
        		o1.write('%s\n' %(cmd))
		        o1.close()

        		cmd='qsub %s' %(outfile)
	        	subprocess.Popen(cmd,shell=True).wait()

	        	if counter%100 == 0:
				print('%i movies submitted...' %(counter))
        	        	time.sleep(400)
			os.remove(outfile)
	        	counter=counter+1

	print('\n%i movies submitted to the cluster for compression using mrc2tif' %(counter-1))
