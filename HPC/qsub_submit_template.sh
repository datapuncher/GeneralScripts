#!/bin/sh

## What shell should your job run in
#PBS -S /bin/bash
## Your job name
#PBS -N MotionCorr2
## Specify: Node, Processors Per Node, Memory Per Proc
#PBS -l nodes=1:ppn=20,pmem=12g
## Specify the maximum amount of time you want your job to run before being killed (If omitted, defaults to 01:00:00 (1 hour))
## Specify in seconds, or [[HH:]MM:]SS
#PBS -l walltime=08:00:00
## Export all environment variables
#PBS -V
## Join stdout and stderr
#PBS -j oe
## Specify which queue to run the job on
##  - "batch" is the default queue (all nodes with <= 256 GB memory)
##  - "himem" consists of machines with >256 GB memory (Currently just 1 machine)
##  - "gpu"   consists of 4 machines each with 2 GTX 1070 cards and 128 GB of memory
##  - "q2014" consists of the 24 computers (480 cores) from the 2014 purchase
##  - "q2015" consists of the 34 computers (680 cores) from the 2015 purchase
#PBS -q gpu
## Where to send any emails
##PBS -M uniquename@umich.edu
## When to send email to the address above
## on job abort (a), when job begins (b), and when job ends (e).
#PBS -m abe

## The following is not required, but will give you a count of assigned cores which is useful when using MPI as in the example below.
NSLOTS=$(wc -l $PBS_NODEFILE|awk {'print $1'})
echo "Got $NSLOTS processors."
echo "I am running on" `hostname`
 
cd $PBS_O_WORKDIR
 
## The mpirun command for legacy OpenMPI releases.
# `which mpirun` -byslot -np $NSLOTS --machinefile $PBS_NODEFILE /path/to/mpi_executable
  
## The mpirun command for OpenMPI releases 1.8 and higher
## The --map-by directive is the preferred method of specifying the distribution of MPI jobs.
## ppr:#:node will launch # number of MPI jobs per node.
# `which mpirun` --map-by ppr:#:node --machinefile $PBS_NODEFILE /path/to/mpi_executable

/lsi/local/packages/openmpi/4.0.2-gcc-4.9.4/bin/mpirun --bind-to none -map-by ppr:2:node makeDDAlignMotionCor2_UCSF.py --bin=1 --align --gpuids=0:1 --ddstartframe=0 --MaskCentrow=0 --MaskCentcol=0 --MaskSizerows=1 --MaskSizecols=1 --Patchrows=5 --Patchcols=5 --Iter=7 --FmRef=0 --Bft_global=500 --Bft_local=100 --alignlabel=a --nrw=1 --runname=ddstack1 --rundir=/lsi/groups/mohilab/cryoem_automation/appion/20feb21a/ddstack/ddstack1 --preset=en --commit --projectid=16 --session=20feb21a --no-rejects --continue --parallel --expid=1760 --jobtype=makeddrawframestack
