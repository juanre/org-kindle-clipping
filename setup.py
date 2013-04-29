#!/usr/bin/env python

from setuptools import setup

setup(name='orgklip',
      version='0.0.1',
      description='Convert Kindle clipplings to org-mode, with links to the original.',
      author='Juan Reyero',
      author_email='juan@juanreyero.com',
      url='http://juanreyero.com/',
      packages=['orgklip'],
      entry_points = {
            'console_scripts': ['bookbib = orgklip.bookid:as_main',
                                'bookclips = orgklip.clipper:as_main']},
      test_suite='orgklip.test.orgklip_test.suite')

