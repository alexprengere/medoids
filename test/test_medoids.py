#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module is the main launcher for tests.
"""

import unittest
import doctest

import os.path as op
import sys

UPDIR = op.split(op.dirname(__file__))[0]
if UPDIR not in sys.path:
    sys.path.append(UPDIR)


import medoids
from medoids import build_distances, k_medoids_iterspawn, k_medoids_iterall


class MedoidsTest(unittest.TestCase):
    def setUp(self):
        self.points = [1, 2, 3, 4, 5, 6, 7]
        self.dists = build_distances(self.points, lambda a, b: abs(b - a))

    def test_medoids_iterspawn(self):
        diam, _ = k_medoids_iterspawn(self.points,
                                      k=2,
                                      dists=self.dists,
                                      spawn=2,
                                      verbose=False)
        self.assertEquals(diam, 3.)

    def test_medoids_iterall(self):
        diam, medoids = k_medoids_iterall(self.points,
                                          diam_max=3,
                                          dists=self.dists,
                                          spawn=3,
                                          verbose=False)
        self.assertEquals(diam, 3.)
        self.assertEquals(len(medoids), 2)



def test_suite():
    """Create a test suite of all doctests.
    """
    s = unittest.TestSuite()

    # Standard options for DocTests
    opt = (doctest.ELLIPSIS |
           doctest.NORMALIZE_WHITESPACE |
           doctest.REPORT_ONLY_FIRST_FAILURE |
           doctest.IGNORE_EXCEPTION_DETAIL)

    points = [1, 2, 3, 4, 5, 6, 7]
    dists = build_distances(points, lambda a, b: abs(b - a))

    globs = {
        'points': points,
        'dists': dists,
    }

    s.addTests(unittest.makeSuite(MedoidsTest))
    s.addTests(doctest.DocTestSuite(medoids, optionflags=opt, extraglobs=globs))
    s.addTests(doctest.DocFileSuite('../README.rst', optionflags=opt))

    return unittest.TestSuite(s)


if __name__ == "__main__":

    # Verbosity is not available for some old unittest version
    #unittest.main(defaultTest='test_suite', verbosity=2)
    unittest.main(defaultTest='test_suite')

