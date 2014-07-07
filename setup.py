from setuptools import setup

setup(name='hpcdo',
      version='0.1',
      description='command line utility to interface with hpc',
      url='https://github.com/tlamadon/hpcdo',
      author='Thibaut Lamadon',
      author_email='thibaut.lamadon@gmail.com',
      license='MIT',
      packages=['hpcdo'],
      scripts=['bin/hpcdo'],
      install_requires=[
        "jinja2",
        "pyaml",
        "paramiko"
        ],
      zip_safe=False)