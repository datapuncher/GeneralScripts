#!/usr/bin/env python

inputfile='cistem_refpack0.star'
phasecol=8

outputfile='%s_degree.star' %(inputfile[:-5])

in1=open(inputfile,'r')
o1=open(outputfile,'w')

for line in in1: 
	if len(line)<40:
		o1.write(line)
		continue
	l=line.split()
	l[phasecol-1]=str(float(l[phasecol-1])*57.295779513)
	newline='\t'.join(l)
	o1.write(newline+'\n')

