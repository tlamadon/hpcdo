__author__ = 'thibautlamadon'

import subprocess,re
import tempfile, shutil, os, yaml

import subprocess,re
import tempfile, shutil, os, yaml

TEMPLATE_MPI_CMD = """
#!/bin/bash

echo "starting qsub script file"
source ~/.bash_profile
date

# here's the SGE directives
# ------------------------------------------
#$ -q batch.q   # <- the name of the Q you want to submit to
#$ -pe mpich {nslots} #  <- load the openmpi parallel env w/ 3 slots
#$ -S /bin/bash   # <- run the job under bash
#$ -N {name} # <- name of the job in the qstat output
#$ -o {logfile} # <- name of the output file.
#$ -e {errfile} # <- name of the stderr file.
#$ -cwd

module load openmpi
module load open64
module load gcc

echo "calling mpirun now"
{command}
"""

class RmpiWrap(object):
  """creates a template qsub file"""
  def __init__(self, name , rfile , n=16):
    self.name    = name
    self.rfile = rfile
    self.logfile = name + '.std'
    self.errfile = name + '.err'
    self.nslots  = n

  def subfile(self):
    return(TEMPLATE_MPI_CMD.format(
      rfile=self.rfile,
      name=self.name,
      logfile=self.logfile,
      errfile=self.errfile,
      nslots=self.nslots))

  def submit(self):
    f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    print "temporay qsub file:",f.name
    f.write(TEMPLATE_MPI_CMD.format(
      rfile=self.rfile,
      name=self.name.lower(),
      logfile=self.logfile.lower(),
      errfile=self.errfile.lower(),
      nslots=self.nslots))
    f.close()
    cmd = subprocess.call(['qsub' , f.name],shell=True, stdout=subprocess.PIPE)
    output = []
    for line in cmd.stdout:
      output.append(line)
    return(output)

class SgeLocalScheduler:
  def __init__(self):
    self.type="localhost"

  def qstat(self):
    cmd = subprocess.Popen("qstat",shell=True, stdout=subprocess.PIPE)
    jobs = {}
    for line in cmd.stdout:
      if "job-ID" in line:
        continue
      if "---------" in line:
        continue
      values = line.split()
      m = re.search('Name: ([a-zA-Z ]*)', line)
      job = {
        "prior":values[1],
        "name":values[2],
        "state":values[4]
      }
      jobs[values[0]] = job
    return jobs

  def submit(self,job):
    """ submits a job
    """
    f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    print "temporay qsub file:",f.name
    f.write(job.getSubFile())
    f.close()
    cmd = subprocess.call(['qsub' , f.name])
#    output = []
#    for line in cmd.stdout:
#      output.append(line)
#    # output is like our job 38517 ("mpi-timing") has been submitted
#    # extract id from output
#    job["id"] = output.split()[2]
    job.id = "1"
    return None

  def clean(self,job):
    subprocess.call(['rm' , job["log"].lower() + ".log"])
    subprocess.call(['rm' , job["log"].lower() + ".err"])

class ClusterList:
  def __init__(self):
    self.path=""


