#!/usr/bin/env python

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
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

if len(sys.argv)!=2: 
	print '\nTo use: ./move_appion_frames_symlink.py [leginon session name]\n'
	sys.exit()

framesdir='/lsi/cryoem_automation/frames/'+sys.argv[1]+'/rawdata/'
newframesdir='/lsi/groups/mcianfroccolab/cryoem_automation/frames/'+sys.argv[1]+'/rawdata/'

if os.path.exists(newframesdir): 
	print 'Error: Destination directory %s already exists. Exiting' %(newframesdir)
	sys.exit()

if not os.path.exists(framesdir): 
	print 'Error: Input frames directory %s does not exist. Exiting' %(framesdir)
	sys.exit()

nummovies=len(glob.glob('%s/*frames.mrc' %(framesdir)))

if nummovies == 0: 
	print 'No movies found in %s. Exiting' %(framesdir)
	sys.exit()

ans=query_yes_no("\nFound %i movies in %s. Do you want to move them to %s? Y/n" %(nummovies,framesdir,newframesdir))

if ans is True: 
	print '\nMoving files...'
	os.makedirs('/lsi/groups/mcianfroccolab/cryoem_automation/frames/'+sys.argv[1])
	os.makedirs('/lsi/groups/mcianfroccolab/cryoem_automation/frames/'+sys.argv[1]+'/rawdata/')

	cmd='mv %s* %s' %(framesdir,newframesdir)
	print cmd 
	subprocess.Popen(cmd,shell=True).wait()	

	print '\nSymbolically linking them back into the frames directory...'
	cmd='ln -s %s* %s' %(newframesdir,framesdir)
	print cmd 
	subprocess.Popen(cmd,shell=True).wait() 

if ans is False:
	delans=query_yes_no("\nDo you want to delete these movies? Y/n")
	if delans is True: 
		print '\nRemoving movies from %s' %(framesdir)
		del2ans=query_yes_no("\nAre you sure? This cannot be undone. Y/n")
		if del2ans is True:
			cmd='rm -f %s*frames.mrc' %(framesdir)
			print cmd 
			subprocess.Popen(cmd,shell=True).wait()    
