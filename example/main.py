__author__ = 'thibautlamadon'


import hpcdo
hpcdo = reload(hpcdo)

YAML_CFG = """
job1:
  name: julia1
  cmd: /data/uctptla/git/julia/julia /data/uctptla/git/Examples/julia/sge/sge.jl
  n: 10
  log: julia1
"""

jobdesc = hpcdo.JobDescriptions(YAML_CFG,file=False)
job1 = jobdesc.getJob("job1")
job1["n"] = 4

sc = hpcdo.SgeLocalScheduler()
sc.submit(job1)

sc.ls()
sc.ls(job1)

sc.tail(job1)
sc.kill(job1)
sc.clean(job1)


# checking template job

jtpl = hpcdo.TemplateJob({"template":"example/cmd.tpl","name":"example"})