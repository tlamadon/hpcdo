__author__ = 'thibautlamadon'

from jinja2 import Template,Environment,FileSystemLoader

class Job:
  id = ""
  desc = {}
  def __init__(self):
    return None
  def __init__(self,desc):
    return None

class CmdJob(Job):
  def __init__(self,desc):
    return None

class TemplateJob():
  id=""
  desc = {}
  def __init__(self,desc):
    self.desc = desc
    return None
  def getSubFile(self):
    # step1, loads the template
    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(self.desc["template"])
    return template.render(self.desc).encode('utf-8')





