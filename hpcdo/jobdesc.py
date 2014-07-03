__author__ = 'thibautlamadon'

import yaml,json

"""
 Deals with loading the description of jobs from a file.
"""

class JobDescriptions:
  content = {}

  def __init__(self):
    self.path=""

  def __init__(self,str='hpc_jobs.yaml',file=True):
    if file:
      with open(str, 'r') as f:
        self.content = yaml.load(f)
    else:
      self.content = yaml.load(str)

  def getJobDesc(self,name):
    return self.content[name]


class JobList:
  """ keeps information about active jobs
  """
  content = {}
  filename = ""

  def __init__(self,file="jobs.json"):
    self.filename = file
    self.reload()

  def reload(self):
    with open(self.filename) as data_file:
      data = json.load(data_file)
    self.content = json.load(data)

  def save(self):
    with open(self.filename, 'w') as outfile:
      json.dump(self.content, outfile)

  def add(self,job):
    self.content[job["id"]] = job
    self.save()

