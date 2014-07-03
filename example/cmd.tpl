#!/bin/bash

echo "starting qsub script file"
source ~/.bash_profile
date

# here's the SGE directives
# ------------------------------------------
#$ -q batch.q   # <- the name of the Q you want to submit to
#$ -pe mpich {{nslots}} #  <- load the openmpi parallel env w/ 3 slots
#$ -S /bin/bash   # <- run the job under bash
#$ -N {{name}} # <- name of the job in the qstat output
#$ -o {{logfile}} # <- name of the output file.
#$ -e {{errfile}} # <- name of the stderr file.
#$ -cwd

module load openmpi
module load open64
module load gcc

echo "calling mpirun now"
{command}