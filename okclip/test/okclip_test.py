"""Integrate unittest and docstring.  Main entry for testing.
"""

import okclip.parse
import okclip.book

import unittest, doctest

def suite():
    tests = [doctest.DocTestSuite(okclip.parse),
             doctest.DocTestSuite(okclip.book)]
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
