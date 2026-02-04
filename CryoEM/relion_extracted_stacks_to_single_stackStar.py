#!/usr/bin/env python
#mpirun -np 20 relion_preprocess_mpi --operate_on Extract/job045/particles.star --operate_out Extract/job045/particles_relion.mrcs
import subprocess
import os
star='Extract/job190/particles_localUVA.star'

outstackname='Extract/job190/particles_localUVA_stack.mrcs'
outstackstar='%s.star' %(outstackname[:-5])
if os.path.exists(outstackstar): 
	os.remove(outstackstar)
staropen=open(star,'r')
o1=open(outstackstar,'w')

partstacklist=[]
counter=1
for line in staropen: 

	if len(line) < 40: 
		o1.write(line)
		continue

	l=line.split()

	partstack=l[5].split('@')[-1]

	if partstack not in partstacklist: 
		partstacklist.append(partstack)

	l[5]='%06i@%s' %(counter,outstackname.split('/')[-1])

	line='\t'.join(l)

	o1.write(line+'\n')

	counter=1+counter

print len(partstacklist)

sys.exit()
for instack in partstacklist: 

	cmd='e2proc2d.py %s %s' %(instack,outstackname)
	subprocess.Popen(cmd,shell=True).wait()

o1.close()
staropen.close()
