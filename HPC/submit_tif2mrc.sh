#!/bin/bash

#PBS -V
#PBS -N tif2mrc
#PBS -k eo
#PBS -q batch
#PBS -l nodes=1:ppn=1
#PBS -l walltime=0:60:00

NSLOTS=$(wc -l $PBS_NODEFILE|awk {"print $1"})
source /Users/jporta/modules.sh
module load imod
cd $PBS_O_WORKDIR

tif2mrc /lsi/groups/mohilab/cryoem_automation/frames/19apr02d/rawdata/19apr02d_grid7_00027gr_00018sq_v02_00003hl_v01_00011en.frames.tif /lsi/groups/mohilab/cryoem_automation/frames/19apr02d/rawdata/19apr02d_grid7_00027gr_00018sq_v02_00003hl_v01_00011en.frames.mrc
