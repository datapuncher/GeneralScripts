#!/bin/bash
#SBATCH --job-name=Subtract/job012/run
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --ntasks=8
#SBATCH --partition=sb-96
#SBATCH --cpus-per-task=1
#SBATCH --error=Subtract/job012/run.err
#SBATCH --output=Subtract/job012/run.out
#SBATCH --open-mode=append
#SBATCH --time=5-00:00:00
#SBATCH --mem-per-cpu=8g
#SBATCH

# Run particle subtraction routine
echo srun --mem-per-cpu=6g --mpi=pmi2 `which relion_particle_subtract_mpi` --i Refine3D/job010/run_it015_optimiser.star --mask MaskCreate/job009/mask.mrc --o Subtract/job012/ --cpu --pipeline_control Subtract/job012/
