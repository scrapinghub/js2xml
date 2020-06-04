#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='js2xml',
      version='0.4.0',
      description='Convert Javascript code to XML document',
      long_description="""
======
js2xml
======

js2xml is a simple helper to parse Javascript code
by representing a parse tree in XML.

You can then use XPath for example to find interesting
bits in Javascript instructions (strings, IDs, function parameters...)

      """,
      author='Paul Tremberth',
      author_email='paul.tremberth@gmail.com',
      packages=find_packages(exclude=['tests']),
      requires=['calmjs.parse', 'lxml'],
      install_requires=[
        "calmjs.parse",
        "lxml",
        "six"
      ],
      classifiers = [
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
     ],
     url = 'https://github.com/scrapinghub/js2xml',
     download_url = 'https://github.com/scrapinghub/js2xml/archive/v0.4.0.tar.gz',
)
