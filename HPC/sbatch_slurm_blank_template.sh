#!/bin/bash

#SBATCH --job-name=XXXnameXXXrun
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --ntasks=XXXmpinodesXXX
#SBATCH --partition=XXXqueueXXX
#SBATCH --cpus-per-task=XXXthreadsXXX
#SBATCH --error=XXXerrfileXXX
#SBATCH --output=XXXoutfileXXX
#SBATCH --open-mode=append
##SBATCH --account=XXXextra1XXX
#SBATCH --time=XXXextra2XXX
#SBATCH --mem-per-cpu=XXXextra3XXX
#SBATCH --gres=XXXextra4XXX
#SBATCH XXXextra5XXX
#SBATCH XXXextra6XXX
#SBATCH XXXextra7XXX

echo srun --mem-per-cpu=XXXextra3XXX --mpi=pmi2 XXXcommandXXX
srun --mem-per-cpu=XXXextra3XXX --mpi=pmi2 XXXcommandXXX

