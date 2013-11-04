"""Integrate unittest and docstring.  Main entry for testing.
"""

import orgklip.parse
import orgklip.docid

import unittest, doctest

def suite():
    tests = [doctest.DocTestSuite(orgklip.parse),
             doctest.DocTestSuite(orgklip.docid)]
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
