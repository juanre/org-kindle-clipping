#!/usr/bin/env python

from setuptools import setup

setup(name='okclip',
      version='0.0.1',
      description='Convert Kindle clipplings to org-mode, with links to the original.',
      author='Juan Reyero',
      author_email='juan@juanreyero.com',
      url='http://juanreyero.com/',
      packages=['okclip'],
      entry_points = {
            'console_scripts': ['bookbib = okclip.bookid:as_main',
                                'bookclips = okclip.clipper:as_main']},
      test_suite='okclip.test.okclip_test.suite')
