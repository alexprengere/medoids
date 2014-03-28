#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module is the main launcher for tests.
"""

import unittest
import doctest

import os
import sys

# PYTHON PATH MANAGEMENT
DIRNAME = os.path.dirname(__file__)
if DIRNAME == '':
    DIRNAME = '.'

DIRNAME = os.path.realpath(DIRNAME)
UPDIR   = os.path.split(DIRNAME)[0]

if UPDIR not in sys.path:
    sys.path.append(UPDIR)


import MedoidsModule



def test_suite():
    """
    Create a test suite of all doctests.
    """

    tests = unittest.TestSuite()

    # Standard options for DocTests
    opt =  (doctest.ELLIPSIS |
            doctest.NORMALIZE_WHITESPACE |
            doctest.REPORT_ONLY_FIRST_FAILURE |
            doctest.IGNORE_EXCEPTION_DETAIL)

    points = [1, 2, 3, 4, 5, 6, 7]
    dists  = MedoidsModule.buildDists(points, MedoidsModule.custom_dist)

    globs = {
        'points': points,
        'dists' : dists
    }

    tests.addTests(doctest.DocTestSuite(MedoidsModule, optionflags=opt, extraglobs=globs))
    tests.addTests(doctest.DocFileSuite('../README.rst', optionflags=opt))


    return unittest.TestSuite(tests)


if __name__ == "__main__":

    # Verbosity is not available for some old unittest version
    #unittest.main(defaultTest='test_suite', verbosity=2)
    unittest.main(defaultTest='test_suite')

