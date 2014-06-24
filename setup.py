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
      zip_safe=False)