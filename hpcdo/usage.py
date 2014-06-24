__author__ = 'thibautlamadon'


#!/usr/bin/python2.6

import subprocess
import re

def finger(login):
  """ get information about a given user
  """
  cmd = subprocess.Popen("finger " + login, shell=True, stdout=subprocess.PIPE)
  for line in cmd.stdout:
    if "Name" in line:
      m = re.search('Name: ([a-zA-Z ]*)', line)
      return(m.group(1))

usage = dict()
cmd = subprocess.Popen('qstat -u "*" -t', shell=True, stdout=subprocess.PIPE)
for line in cmd.stdout:
  if "a_shephard" in line:
    cur_user = "a_shephard"
    if cur_user not in usage.keys():
      usage[cur_user]=dict()
  if "uctp" in line:
    m = re.search('(uctp[a-z0-9]*) ', line)
    if m is None:
      continue
    cur_user = m.group(1)
    if cur_user not in usage.keys():
      usage[cur_user]=dict()
  if "@node" in line:
    m = re.search('node([0-9]*).ic', line)
    if m is None:
      continue
    if m.group(1) in usage[cur_user]:
      usage[cur_user][m.group(1)]+=1
    else:
      usage[cur_user][m.group(1)]=1

hosts = dict()
cmd = subprocess.Popen('qhost', shell=True, stdout=subprocess.PIPE)
for line in cmd.stdout:
  if "node" not in line:
    continue
  s = [i for i in line.split(' ') if len(i) >0]
  hosts[s[0]] = {'load':s[3],'n':s[2]}

# printing

for (user, nodes) in usage.items():
  waste = 0
  total = 0
  for (node , load) in nodes.items():
    if (hosts["node" + node]['load']=='-'):
      continue
    total += load
    if float(load)>float(hosts["node" + node]['load']):
      waste += float(load) - float(hosts["node" + node]['load'])
  print user.ljust(12), " uses ", str(total).ljust(10), " wastes ", str(waste).ljust(10) , finger(user)
