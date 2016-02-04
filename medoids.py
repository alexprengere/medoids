#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module handles the clustering, from a general matter.
We have a list of elements and a structure containing their distance,
like dists[p][q] = dists[q][p] = || q - p ||::

    >>> points = [1, 2, 3, 4, 5, 6, 7]
    >>> dists = build_distances(points, lambda a, b: abs(b - a))
    >>> dists
    {1: {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}, 2: {1: 1,...

Then we have an implementation of the k-medoids algorithm::

    >>> medoids, diam = k_medoids_iterspawn(points, k=2, dists=dists, spawn=2) #doctest: +SKIP
    * New chosen kernels: [4, 7]
    * Iteration over after 3 steps
    * New chosen kernels: [6, 5]
    * Iteration over after 4 steps
    -- Spawn end: best diameter 3.000, best medoids: [Medoid(2, [1, 2, 3, 4]), Medoid(6, [5, 6, 7])]

And a version which increases automatically the number of clusters till
we have homogeneous clusters::

    >>> medoids, diam = k_medoids_iterall(points, diam_max=3, dists=dists, spawn=2) #doctest: +SKIP
    * New chosen kernels: [6]
    * Iteration over after 2 steps
    * New chosen kernels: [7]
    * Iteration over after 2 steps
    -- Spawn end: best diameter 6.000, best medoids: [Medoid(4, [1, 2, 3, 4, 5, 6, 7])]
    +++ Diameter too bad 6.000 > 3.000
    +++ Going to 2 clusters
    <BLANKLINE>
    * New chosen kernels: [2, 5]
    * Iteration over after 1 steps
    * New chosen kernels: [7, 3]
    * Iteration over after 3 steps
    -- Spawn end: best diameter 3.000, best medoids: [Medoid(2, [1, 2, 3]), Medoid(5, [4, 5, 6, 7])]
    +++ Diameter ok 3.000 ~ 3.000
    +++ Stopping, 2 clusters enough (7 points initially)

"""

from __future__ import with_statement, print_function

import random
from operator import itemgetter
from collections import defaultdict


class Medoid(object):
    __slots__ = ['kernel', 'elements']

    def __init__(self, kernel, elements=None):
        self.kernel = kernel
        self.elements = [] if elements is None else elements

    def __repr__(self):
        return 'Medoid({0}, {1})'.format(self.kernel, self.elements)


def build_distances(points, distance):
    """
    From a list of elements and a function to compute
    the distance between two of them, build the necessary structure
    which is required to perform k-medoids.
    This is like a cache of all distances between all points.

    :param points:   the list of elements
    :param distance: a function able to do distance(a, b) = || b - a ||
    :returns:        the structure containing all distances, it is \
        a dictionary of dictionary, that verifies: \
         res[a][b] = res[b][a] = distance(a, b)

    >>> from pprint import pprint
    >>> points = [1, 2, 3]
    >>> pprint(build_distances(points, lambda a, b: abs(b - a)), width=60)
    {1: {1: 0, 2: 1, 3: 2},
     2: {1: 1, 2: 0, 3: 1},
     3: {1: 2, 2: 1, 3: 0}}
    """
    dists = defaultdict(dict)
    for p in points:
        for q in points:
            dists[p][q] = distance(p, q)
            dists[q][p] = dists[p][q]

    return dict(dists)


def k_medoids(points, k, dists, iteration=20, verbose=True):
    """Standard k-medoids algorithm.

    :param points:    the list of points
    :param k:         the number of clusters
    :param dists:     the cache of distances dists[p][q] = || q - p ||
    :param iteration: the maximum number of iterations
    :param verbose:   verbosity
    :returns:         the partition, structured as \
        a list of [kernel of the cluster, [elements in the cluster]]

    >>> diam, medoids = k_medoids(points, k=2, dists=dists, verbose=True) #doctest: +SKIP
    * New chosen kernels: [5, 6]
    * Iteration over after 3 steps
    """
    if k > len(points):
        k = len(points)

    # Medoids initialization
    medoids = [Medoid(p) for p in random.sample(points, k)]
    if verbose:
        print('* New chosen kernels: {0}'.format([m.kernel for m in medoids]))

    for n in xrange(iteration):
        # Resetting medoids
        for m in medoids:
            m.elements = []

        # Putting points in closest medoids
        for p in points:
            closest = min(medoids, key=lambda m: dists[p][m.kernel])
            closest.elements.append(p)

        # Removing empty medoids
        medoids = [m for m in medoids if m.elements]

        # Electing new kernels for each medoids
        change = False
        for m in medoids:
            center = min(m.elements, key=lambda k: sum(dists[e][k] for e in m.elements))
            if m.kernel != center:
                m.kernel = center
                change = True

        if not change:
            if verbose:
                print('* Iteration over after {0} steps'.format(1 + n))
            break

    diam = max(dists[a][b]
               for m in medoids
               for a in m.elements
               for b in m.elements)

    return diam, medoids


def k_medoids_iterspawn(points, k, dists, spawn=1, iteration=20, verbose=True):
    """
    Same as k_medoids, but we iterate also
    the spawning process.
    We keep the minimum of the biggest diam as a
    reference for the best spawn.

    :param points:    the list of points
    :param k:         the number of clusters
    :param dists:     the cache of distances dists[p][q] = || q - p ||
    :param spawn:     the number of spawns
    :param iteration: the maximum number of iterations
    :param verbose:   boolean, verbosity status
    :returns:         the partition, structured as \
        a list of [kernel of the cluster, [elements in the cluster]]

    >>> diam, medoids = k_medoids_iterspawn(points, k=2, dists=dists, spawn=2)  #doctest: +SKIP
    * New chosen kernels: [5, 1]
    * Iteration over after 1 steps
    * New chosen kernels: [2, 6]
    * Iteration over after 1 steps
    -- Spawn end: best diameter 3.000, best medoids: [Medoid(2, [1, 2, 3, 4]), Medoid(6, [5, 6, 7])]
    """
    # Here the result of k_medoids function is a tuple
    # containing in the second element the diameter of the
    # biggest medoid, so the min function will return
    # the best medoids arrangement, in the sense that the
    # diameter max will ne minimum
    diam, medoids = min(
        (k_medoids(points, k, dists, iteration, verbose) for _ in xrange(spawn)),
        key=itemgetter(0))

    if verbose:
        print('-- Spawn end: best diameter {0:.3f}, best medoids: {1}'.format(diam, medoids))

    return diam, medoids


def k_medoids_iterall(points, diam_max, dists, spawn=1, iteration=20, verbose=True):
    """
    Same as k_medoids_iterspawn, but we increase
    the number of clusters till we have a good enough
    similarity between paths.

    :param points:     the list of points
    :param diam_max: the maximum diameter allowed, otherwise \
        the algorithm will start over and increment the number of clusters
    :param dists:      the cache of distances dists[p][q] = || q - p ||
    :param spawn:      the number of spawns
    :param iteration:  the maximum number of iterations
    :param verbose:    verbosity
    :returns:          the partition, structured as \
        a list of [kernel of the cluster, [elements in the cluster]]

    >>> diam, medoids = k_medoids_iterall(points, diam_max=3, dists=dists, spawn=3) #doctest: +SKIP
    * New chosen kernels: [4]
    * Iteration over after 1 steps
    * New chosen kernels: [3]
    * Iteration over after 2 steps
    * New chosen kernels: [7]
    * Iteration over after 2 steps
    -- Spawn end: best diameter 6.000, best medoids: [Medoid(4, [1, 2, 3, 4, 5, 6, 7])]
    +++ Diameter too bad 6.000 > 3.000
    +++ Going to 2 clusters
    <BLANKLINE>
    * New chosen kernels: [1, 3]
    * Iteration over after 3 steps
    * New chosen kernels: [5, 6]
    * Iteration over after 3 steps
    * New chosen kernels: [7, 6]
    * Iteration over after 4 steps
    -- Spawn end: best diameter 3.000, best medoids: [Medoid(2, [1, 2, 3]), Medoid(5, [4, 5, 6, 7])]
    +++ Diameter ok 3.000 ~ 3.000
    +++ Stopping, 2 clusters enough (7 points initially)
    """
    if not points:
        raise ValueError('No points given!')

    for k, _ in enumerate(points):
        diam, medoids = k_medoids_iterspawn(points, 1 + k, dists, spawn, iteration, verbose)
        if diam <= diam_max:
            break

        if verbose:
            print('+++ Diameter too bad {0:.3f} > {1:.3f}'.format(diam, diam_max))
            print('+++ Going to {0} clusters\n'.format(2 + k))

    if verbose:
        print('+++ Diameter ok {0:.3f} ~ {1:.3f}'.format(diam, diam_max))
        print('+++ Stopping, {0} clusters enough ({1} points initially)'.format(1 + k, len(points)))

    return diam, medoids


def _test():
    """When called directly, launching doctests.
    """
    import doctest

    opt = (doctest.ELLIPSIS |
           doctest.NORMALIZE_WHITESPACE |
           doctest.REPORT_ONLY_FIRST_FAILURE)
           #doctest.IGNORE_EXCEPTION_DETAIL)

    points = [1, 2, 3, 4, 5, 6, 7]
    dists = build_distances(points, lambda a, b: abs(b - a))

    globs = {
        'points': points,
        'dists' : dists
    }

    doctest.testmod(optionflags=opt,
                    extraglobs=globs,
                    verbose=False)


if __name__ == '__main__':
    _test()
