#!/bin/bash

###Inherit all current environment variables
#PBS -V
### Job name
#PBS -N XXXnameXXXrun
### Keep Output and Error
#PBS -k eo
### Queue name
#PBS -q XXXqueueXXX
### Specify the number of nodes and thread (ppn) for your job.
#PBS -l nodes=XXXmpinodesXXX:ppn=XXXdedicatedXXX
### Tell PBS the anticipated run-time for your job, where walltime=HH:MM:SS
#PBS -l walltime=XXXextra1XXX:00:00
#################################
NSLOTS=$(wc -l $PBS_NODEFILE|awk {'print $1'})

### Switch to the working directory;
source /Users/jporta/modules.sh

#module load relion/2.1-beta_cu8.0

cd $PBS_O_WORKDIR
### Run:
mpirun --map-by node -np $NSLOTS XXXcommandXXX > XXXnameXXXrun.out 2> XXXnameXXXrun.err < /dev/null
echo "done"
