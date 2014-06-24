__author__ = 'thibautlamadon'

from shovel import task
import os
from subprocess import call, Popen
import random
import string
import subprocess
import tempfile, shutil, os
import paramiko

TEMPLATE_MPI = """
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

RSNOW=`Rscript -e "cat(.libPaths()[[1]])"`

echo "calling mpirun now"
mpirun -np {nslots}  $RSNOW/snow/RMPISNOW -q < {rfile} > {name}.out
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
    return(TEMPLATE_MPI.format(
      rfile=self.rfile,
      name=self.name,
      logfile=self.logfile,
      errfile=self.errfile,
      nslots=self.nslots))

  def submit(self):
    f = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    print "temporay qsub file:",f.name
    f.write(TEMPLATE_MPI.format(
      rfile=self.rfile,
      name=self.name.lower(),
      logfile=self.logfile.lower(),
      errfile=self.errfile.lower(),
      nslots=self.nslots))
    f.close()
    subprocess.call(['qsub' , f.name])

def hpcConnect():
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect('hpc.econ.ucl.ac.uk',
              username='uctptla',
              key_filename='/Users/thibautlamadon/.ssh/thibaut.lamadon')
  return(ssh)


# shovel tasks
@task
def estimate(educ='educ3',n=16):
  ''' start mpi estimation for given education group '''
  print "running with educ=",educ
  subprocess.call(['rm','-f',"tibo-%s-jmp.*" % educ])
  subprocess.call(['touch',"tibo-%s-jmp.out" % educ])
  subprocess.call(['touch',"tibo-%s-jmp.err" % educ])
  rmpi = RmpiWrap( "TIBO-%s-jmp" % educ.upper(),  "estimate-%s.r" % educ , n )
  rmpi.submit()


# shovel tasks
@task
def tail(educ='educ3'):
  ''' start mpi estimation for given education group '''
  print "tailing ",educ
  subprocess.call(['tail' , '-f', "tibo-%s-jmp.out" % educ , '-f', "tibo-%s-jmp.err" % educ ])


# shovel tasks
@task
def get(name):
  ''' get a file '''

  files = {
    "educ1": {
      "remote" : "/data/uctptla/git/wagebc/Rdata/evaluations.educ1.dat",
      "local"  : "params.educ1.dat"
    },
    "educ3": {
      "remote" : "/data/uctptla/git/wagebc/Rdata/evaluations.educ3.dat",
      "local"  : "params.educ3.dat"
    },
    }

  if (name not in files.keys()):
    print "unknown file"
    return

  ssh = hpcConnect()
  ftp = ssh.open_sftp()
  ftp.get(files[name]['remote'], files[name]['local'])

