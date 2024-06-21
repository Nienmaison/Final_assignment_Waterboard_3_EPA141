#!/bin/bash

#SBATCH --job-name="mbdm_dc"
#SBATCH --time=02:30:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=48
#SBATCH --partition=compute
#SBATCH --mem-per-cpu=2GB
#SBATCH --account=education-tpm-msc-epa

module load 2023r1
module load openmpi
module load python
module load py-numpy
module load py-scipy
module load py-mpi4py
module load py-pip

pip install --user --upgrade ema_workbench

srun python dike_model_optimization_project_1.py > simulation.log
