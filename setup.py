#!/usr/bin/env python

from setuptools import setup, find_packages

version = "0.1"
DESCRIPTION      = 'A combat simulator'
LONG_DESCRIPTION = open('README.txt').read()

setup(name             = 'CombatWiz'       ,
      version          = version           ,
      description      = DESCRIPTION       ,
      long_description = LONG_DESCRIPTION  ,
      author           = 'Ben Farmer, Ken Farmer',
      author_email     = 'kenfar@gmail.com',
      url              = 'http://github.com/kenfar/CombatSim',
      license          = 'BSD'             ,
      classifiers=[
            'Development Status :: 3 - Alpha'                        ,
            'Environment :: Console'                                 ,
            'License :: OSI Approved :: BSD License'                 ,
            'Programming Language :: Python'                         ,
            'Operating System :: POSIX'                              ,
            'Topic :: Games/Entertainment :: Role-Playing'           ,
            'Topic :: Games/Entertainment :: Simulation'
            ],
      download_url = 'http://github.com/downloads/kenfar/CombatWiz/CombatWiz-%s.tar.gz' % version,
      scripts      = ['scripts/combatwiz'         ],
      install_requires     = ['appdirs    >= 1.1.0' ,
                              'pytester'            ,
                              'tox'                 ,
                              'unittest2'          ],
      packages     = find_packages(),
     )
