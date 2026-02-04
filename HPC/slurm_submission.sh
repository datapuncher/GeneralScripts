#!/bin/bash
#SBATCH -N 1
#SBATCH -p gpu
#SBATCH --ntasks-per-node 36
#SBATCH -t 25:00:00

#SBATCH --gres=gpu:l40sgpu
# echo commands to stdout
set -x

hostname
nvidia-smi
