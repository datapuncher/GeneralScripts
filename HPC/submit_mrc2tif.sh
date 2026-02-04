#!/usr/bin/bash

#PBS -V
#PBS -N mrc2tif
#PBS -k eo
#PBS -q batch
#PBS -l nodes=1:ppn=1
#PBS -l walltime=0:60:00

NSLOTS=$(wc -l $PBS_NODEFILE|awk {"print $1"})

# Source 'modules.sh' and load IMOD module
source /Users/jporta/modules.sh
module load imod

# Change to working directory
cd $PBS_O_WORKDIR

# Job run
mrc2tif -s -c zip /lsi/groups/mohilab/cryoem_automation/frames/17aug09a/rawdata/17aug09a_grid_00081gr_00028sq_00002hl_00002ed.frames.mrc /lsi/groups/mohilab/cryoem_automation/frames/17aug09a/rawdata/17aug09a_grid_00081gr_00028sq_00002hl_00002ed.frames.tif

rm /lsi/groups/mohilab/cryoem_automation/frames/17aug09a/rawdata/17aug09a_grid_00081gr_00028sq_00002hl_00002ed.frames.mrc
