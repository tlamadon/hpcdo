__author__ = 'thibautlamadon'

from shovel import task
import os
from subprocess import call, Popen
import random
import string
import subprocess
import tempfile, shutil, os
import paramiko


def hpcConnect():
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect('hpc.econ.ucl.ac.uk',
              username='uctptla',
              key_filename='/Users/thibautlamadon/.ssh/thibaut.lamadon')
  return(ssh)

def estimate(educ='educ3',n=16):
  ''' start mpi estimation for given education group '''
  print "running with educ=",educ
  subprocess.call(['rm','-f',"tibo-%s-jmp.*" % educ])
  subprocess.call(['touch',"tibo-%s-jmp.out" % educ])
  subprocess.call(['touch',"tibo-%s-jmp.err" % educ])
  rmpi = RmpiWrap( "TIBO-%s-jmp" % educ.upper(),  "estimate-%s.r" % educ , n )
  rmpi.submit()


def tail(educ='educ3'):
  ''' start mpi estimation for given education group '''
  print "tailing ",educ
  subprocess.call(['tail' , '-f', "tibo-%s-jmp.out" % educ , '-f', "tibo-%s-jmp.err" % educ ])

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

