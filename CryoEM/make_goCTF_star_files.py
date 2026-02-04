#!/usr/bin/env python
import glob 
import shutil 

indir='/lsi/groups/mcianfroccolab/mcianfro/prex/18aug03b/warp_particles_relion/Extract/job019/average'

for star in glob.glob('%s/*extract.star' %(indir)): 
	shutil.copyfile(star,'%s_go.star' %(star[:-13]))
