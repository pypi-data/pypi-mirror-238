#!/usr/bin/env python

from distutils.core import setup

version = '2.1.1'

long_description = "Adapter for database access"

setup(name='idbadapter',
      version='2.1.1',
      description='Adapter for database access',
      long_description=long_description,
      url="https://github.com/AnatolyPershinov/gpn_cache_module",
      download_url='https://github.com/AnatolyPershinov/gpn_cache_module/archive/master.zip',
      author='Anatoly Pershinov',
      author_email='anatoliypershinov@gmail.com',
      packages=['idbadapter'],
      install_requires=['pandas', 'sqlalchemy', 'psycopg2-binary'],
      classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            ]
      )