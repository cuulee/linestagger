#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='linestagger',
      version='1.0',
      description='Staggers lines to strattle a middle or center line',
      author='Bennett Murphy',
      author_email='murphy214@live.marshall.edu',
      url='https://github.com/murphy214/linestagger',
      install_requires = ['nlgeojson',
      						'simplejson',
      						'pandas',
      						'numpy'],
	  py_modules=['linestagger']
)

