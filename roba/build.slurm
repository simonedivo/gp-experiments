#!/bin/bash

#SBATCH --job-name=gp-exp
#SBATCH --partition=long2
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64

module load singularity/3.4.1
chmod 777 ./runscripts/*.sh
singularity run general.sif ./runscripts/runscript.sh
