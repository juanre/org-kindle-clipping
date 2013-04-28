"""Integrate unittest and docstring.  Main entry for testing.
"""

import okclip.parse
import okclip.bookid

import unittest, doctest

def suite():
    tests = [doctest.DocTestSuite(okclip.parse),
             doctest.DocTestSuite(okclip.bookid)]
    return unittest.TestSuite(tests)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
