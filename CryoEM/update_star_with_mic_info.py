#!/usr/bin/env python
import linecache 
import glob
import sys 

instar='cryosparc_exp000660_005.star'
micdir='average'
particledir='matching'
warpextension='_BoxNet2_20180602.mrcs'
newstar='%s_newmic.star' %(instar[:-5])

miclist=glob.glob('%s/*.mrc' %(micdir))

o1=open(newstar,'w')

for line in open(instar,'r'): 

	if len(line)<40: 
		o1.write(line)
		continue
	particlename=line.split()[10].split("@")[-1].split('/')[-1]
	micname='%s/%s.mrc' %(micdir,particlename[:-len(warpextension)])
	partnum=float(line.split()[10].split("@")[0].strip())

	#Get part num x & y coord
	linenum=8+int(partnum)
	coordline=linecache.getline('%s/%s.star' %(particledir,particlename[:-5]),linenum)
	if len(coordline.split()) != 4: 
		print coordline
		print len(coordline.split())
		print '%s/%s.star' %(particledir,particlename[:-5])
		print micname
		print partnum
		print linenum
		print particlename
		print 'error'		
		sys.exit()
	rlnx=coordline.split()[0]
	rlny=coordline.split()[1]

	l=line.split()
	l='\t'.join(l)+'\t'+micname+'\t'+rlnx+'\t'+rlny+'\n'
	o1.write(l)


