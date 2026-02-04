#!/usr/bin/env python

file_choosing_from='cryosparc_exp000135_003.star'
imagename_file_choosing_from=11
file_to_update='Extract/job078/particles_scale_mag_apix.star'
imagename_file_to_update=6
ext_to_remove='_scale.mrcs'

#read particles into list
sellist=[]
for line in open(file_choosing_from,'r'): 
	if len(line)<40:
		continue
	sellist.append(line.split()[imagename_file_choosing_from-1])
print sellist

o1=open('%s_sel.star' %(file_to_update[:-5]),'w')

for line in open(file_to_update,'r'): 	

	if len(line)<40:
		o1.write(line)
		continue
	check=line.split()[imagename_file_to_update-1][:-len(ext_to_remove)]+'.mrcs'
	check=check.replace('job078','job063')
	if check in sellist: 
		o1.write(line)


