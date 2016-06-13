#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module is the main launcher for tests.
"""

import unittest
import doctest

import medoids
from medoids import k_medoids, k_medoids_auto_k


class MedoidsTest(unittest.TestCase):
    def setUp(self):
        self.points = [1, 2, 3, 4, 5, 6, 7]
        self.distance = lambda a, b: abs(b - a)

    def test_medoids_iterspawn_1(self):
        diam, _ = k_medoids(self.points,
                            k=1,
                            distance=self.distance,
                            spawn=2,
                            verbose=False)
        self.assertEquals(diam, 6.)

    def test_medoids_iterspawn_2(self):
        diam, _ = k_medoids(self.points,
                            k=2,
                            distance=self.distance,
                            spawn=2,
                            verbose=False)
        self.assertEquals(diam, 3.)

    def test_medoids_iterspawn_3(self):
        diam, _ = k_medoids(self.points,
                            k=7,
                            distance=self.distance,
                            spawn=2,
                            verbose=False)
        self.assertEquals(diam, 0.)

    def test_medoids_iterall_1(self):
        diam, medoids = k_medoids_auto_k(self.points,
                                         diam_max=3,
                                         distance=self.distance,
                                         spawn=3,
                                         verbose=False)
        self.assertEquals(diam, 3.)
        self.assertEquals(len(medoids), 2)

    def test_medoids_iterall_2(self):
        diam, medoids = k_medoids_auto_k(self.points,
                                         diam_max=0,
                                         distance=self.distance,
                                         spawn=3,
                                         verbose=False)
        self.assertEquals(diam, 0.)
        self.assertEquals(len(medoids), 7)


def test_suite():
    """Create a test suite of all doctests."""
    s = unittest.TestSuite()

    # Standard options for DocTests
    opt = (doctest.ELLIPSIS |
           doctest.NORMALIZE_WHITESPACE |
           doctest.REPORT_ONLY_FIRST_FAILURE |
           doctest.IGNORE_EXCEPTION_DETAIL)

    globs = {
        'points': [1, 2, 3, 4, 5, 6, 7],
        'distance': lambda a, b: abs(b - a),
    }

    s.addTests(unittest.makeSuite(MedoidsTest))
    s.addTests(doctest.DocTestSuite(medoids, optionflags=opt, extraglobs=globs))
    s.addTests(doctest.DocFileSuite('./README.rst', optionflags=opt))

    return unittest.TestSuite(s)


if __name__ == "__main__":
    # Verbosity is not available for some old unittest version
    # unittest.main(defaultTest='test_suite', verbosity=2)
    unittest.main(defaultTest='test_suite')
