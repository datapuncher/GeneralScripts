#!/usr/bin/env python

infile='CtfFind/job100/micrographs_ctf.star'
outfile='%s_sel_res9_df13_50.star' %(infile[:-5])
reslim=9
dfupper=50000
dflower=13000
dfcolnum=3
rescolnum=12

o1=open(infile,'r')
out=open(outfile,'w')

for line in o1: 

	if len(line) < 40: 
		out.write(line)
		continue
	res=float(line.split()[rescolnum-1])
	df=float(line.split()[dfcolnum-1])
	if res<reslim: 
		if df>dflower: 
			if df<dfupper: 
				out.write(line)

o1.close()
