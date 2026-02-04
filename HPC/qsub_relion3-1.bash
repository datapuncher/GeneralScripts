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
#PBS -l walltime=72:00:00
#################################
NSLOTS=$(wc -l $PBS_NODEFILE|awk {'print $1'})

in_cmd='XXXcommandXXX'

module purge 

if [ XXXqueueXXX == "gpu" ]; then
        module load relion/3.1beta-cluster/gpu/openmpi/4.0.2
	module load cuda/9.0 
        if grep -q relion_refine <<<$in_cmd; then
        	NSLOTS=5
	        cmd_to_run="${in_cmd/'`which relion_refine`'/relion_refine_mpi}"
        fi
	if grep -q relion_autopick <<<$in_cmd; then
                NSLOTS=5
                cmd_to_run="${in_cmd/'`which relion_autopick`'/relion_autopick_mpi}"
        fi
	if grep -q relion_run_ctffind <<<$in_cmd; then
        	NSLOTS=4
	        cmd_to_run="${in_cmd/'`which relion_run_ctffind`'/relion_run_ctffind_mpi}"
        fi
	if grep -q 'gpu "0:1:2:3"' <<<$cmd_to_run; then
		cmd_to_run="${cmd_to_run/'"0:1:2:3"'/0:1:2:3}"
	fi
	if grep -q 'gpu ""' <<<$cmd_to_run; then
                cmd_to_run="${cmd_to_run/'""'/0:1:2:3}"
        fi
fi

if [ XXXqueueXXX == "batch" ]; then
        module purge 
	module load relion/3.1beta-cluster/openmpi/4.0.2
	if grep -q relion_refine <<<$in_cmd; then
                cmd_to_run="${in_cmd/'`which relion_refine_mpi`'/relion_refine_mpi}"
        fi
	if grep -q relion_autopick <<<$in_cmd; then
                cmd_to_run="${in_cmd/'`which relion_autopick_mpi`'/relion_autopick_mpi}"
        fi
	if ! grep -q relion_preproess_mpi <<<$in_cmd; then
                cmd_to_run="${in_cmd/'`which relion_preprocess_mpi`'/relion_preprocess_mpi}"
        fi
	if grep -q relion_ctf_refine_mpi <<<$in_cmd; then
                cmd_to_run="${in_cmd/'`which relion_ctf_refine_mpi`'/relion_ctf_refine_mpi}"
        fi
	if grep -q relion_motion_refine <<<$in_cmd; then
                cmd_to_run="${in_cmd/'`which relion_motion_refine`'/relion_motion_refine}"
        fi
	if grep -q relion_motion_refine_mpi <<<$in_cmd; then
                cmd_to_run="${in_cmd/'`which relion_motion_refine_mpi`'/relion_motion_refine_mpi}"
	fi
	if grep -q relion_run_motioncorr_mpi <<<$in_cmd; then
		cmd_to_run="${in_cmd/'`which relion_run_motioncorr_mpi`'/relion_run_motioncorr_mpi}"
	fi
	if grep -q relion_particle_subtract_mpi <<<$in_cmd; then
		cmd_to_run="${in_cmd/'`which relion_particle_subtract_mpi`'/relion_particle_subtract_mpi}"
	fi
	if grep -q relion_refine_mpi <<<$in_cmd; then
		cmd_to_run="${in_cmd/'`which relion_refine_mpi`'/relion_refine_mpi}"
	fi
	if grep -q relion_run_ctffind_mpi <<<$in_cmd; then
		cmd_to_run="${in_cmd/'`which relion_run_ctffind_mpi`'/relion_run_ctffind_mpi}"
	fi
fi
if grep -q relion_autopick_mpi <<<$in_cmd; then
	cmd_to_run="${in_cmd/'`which relion_autopick_mpi`'/relion_autopick_mpi}"
fi

cd $PBS_O_WORKDIR
### Run:
echo $cmd_to_run >> XXXnameXXXrun.out
mpirun -np $NSLOTS $cmd_to_run >> XXXnameXXXrun.out 2>> XXXnameXXXrun.err < /dev/null
echo "done"
