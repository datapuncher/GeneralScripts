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
#PBS -l nodes=XXXextra2XXX:ppn=XXXdedicatedXXX
### Tell PBS the anticipated run-time for your job, where walltime=HH:MM:SS
#PBS -l walltime=XXXextra1XXX:00:00
#################################
NSLOTS=$(wc -l $PBS_NODEFILE | awk {'print $1'})

in_cmd='XXXcommandXXX'

module purge

# The job should run on GPUs
if [ XXXqueueXXX == "gpu" ]; then
    module load relion/3.0.8-cluster/gpu/openmpi/4.0.2
    if grep -q relion_refine\` <<< $in_cmd; then
        NSLOTS=5
        cmd_to_run="${in_cmd/relion_refine\`/relion_refine_mpi\`}"
    fi
    if grep -q relion_run_ctffind\` <<< $in_cmd; then
        NSLOTS=4
        cmd_to_run="${in_cmd/relion_run_ctffind\`/relion_run_ctffind_mpi\`}"
    fi
fi

# The job should run on CPUs
if [ XXXqueueXXX == "batch" ]; then
    module load relion/3.0.8-cluster/openmpi/4.0.2
    if grep -q relion_refine\` <<< $in_cmd; then
        cmd_to_run="${in_cmd/relion_refine\`/relion_refine_mpi\`}"
    fi
fi

if [ -z "${cmd_to_run}" ]; then
    cmd_to_run="${in_cmd}"
fi

cd $PBS_O_WORKDIR

# Run:
echo $cmd_to_run >> XXXnameXXXrun.out
echo "Starting at $(date)" >> XXXnameXXXrun.out
if grep -q _mpi <<< $in_cmd; then
    eval "mpirun --map-by ppr:XXXextra3XXX:node ${cmd_to_run} >> XXXnameXXXrun.out 2>> XXXnameXXXrun.err < /dev/null"
else
    eval "${cmd_to_run} >> XXXnameXXXrun.out 2>> XXXnameXXXrun.err < /dev/null"
fi
echo "Ended at $(date)" >> XXXnameXXXrun.out
echo "done"

