#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
K medoids implementation based on a matrix of distances.
"""

#pylint: disable=undefined-loop-variable
from __future__ import with_statement, print_function

import random
from operator import itemgetter
from collections import defaultdict

MAX_ITER = int(1e3)


class Medoid(object):
    __slots__ = ['kernel', 'elements']

    def __init__(self, kernel, elements=None):
        self.kernel = kernel
        self.elements = [] if elements is None else elements

    def __repr__(self):
        return 'Medoid({0}, {1})'.format(self.kernel, self.elements)

    def __iter__(self):
        return iter(self.elements)

    def compute_kernel(self, dists):
        return min(self, key=lambda e: sum(dists[e][other] for other in self))

    def compute_diameter(self, dists):
        return max(dists[a][b] for a in self for b in self)


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


def k_medoids(points, k, dists, max_iterations=MAX_ITER, verbose=True):
    """Standard k-medoids algorithm.

    :param points:    the list of points
    :param k:         the number of clusters
    :param dists:     the cache of distances dists[p][q] = || q - p ||
    :param max_iterations: the maximum number of iterations
    :param verbose:   verbosity
    :returns:         the partition, structured as \
        a list of [kernel of the cluster, [elements in the cluster]]

    >>> diam, medoids = k_medoids(points, k=2, dists=dists, verbose=True)
    * New chosen kernels: [6, 3]
    * Iteration over after 3 steps, max diameter 3
    """
    if k > len(points):
        raise ValueError('Number of medoids exceeds number of points')

    # Medoids initialization
    medoids = [Medoid(kernel=p) for p in random.sample(points, k)]
    if verbose:
        print('* New chosen kernels: {0}'.format([m.kernel for m in medoids]))

    for n in xrange(1, 1 + max_iterations):
        # Resetting medoids
        for m in medoids:
            m.elements = []

        # Putting points in closest medoids
        for p in points:
            closest_medoid = min(medoids, key=lambda m: dists[m.kernel][p])
            closest_medoid.elements.append(p)

        # Removing empty medoids
        medoids = [m for m in medoids if m.elements]

        # Electing new kernels for each medoids
        change = False
        for m in medoids:
            new_kernel = m.compute_kernel(dists)
            if new_kernel != m.kernel:
                m.kernel = new_kernel
                change = True

        if not change:
            break

    diam = max(m.compute_diameter(dists) for m in medoids)
    if verbose:
        print('* Iteration over after {0} steps, max diameter {1}'.format(n, diam))

    return diam, medoids


def k_medoids_iterspawn(points, k, dists, spawn, max_iterations=MAX_ITER, verbose=True):
    """
    Same as k_medoids, but we iterate also
    the spawning process.
    We keep the minimum of the biggest diam as a
    reference for the best spawn.

    :param points:    the list of points
    :param k:         the number of clusters
    :param dists:     the cache of distances dists[p][q] = || q - p ||
    :param spawn:     the number of spawns
    :param max_iterations: the maximum number of iterations
    :param verbose:   boolean, verbosity status
    :returns:         the partition, structured as \
        a list of [kernel of the cluster, [elements in the cluster]]

    >>> diam, medoids = k_medoids_iterspawn(points, k=2, dists=dists, spawn=2)
    * New chosen kernels: [2, 3]
    * Iteration over after 3 steps, max diameter 3
    * New chosen kernels: [1, 2]
    * Iteration over after 4 steps, max diameter 3
    ~~ Spawn end: min of max diameters 3.000 for medoids: [Medoid(2, [1, 2, 3]), Medoid(5, [4, 5, 6, 7])]
    """
    kw = {
        'points': points,
        'k': k,
        'dists': dists,
        'max_iterations': max_iterations,
        'verbose': verbose,
    }
    # Here the result of k_medoids function is a tuple
    # containing in the second element the diameter of the
    # biggest medoid, so the min function will return
    # the best medoids arrangement, in the sense that the
    # diameter max will be minimum
    diam, medoids = min((k_medoids(**kw) for _ in xrange(spawn)), key=itemgetter(0))
    if verbose:
        print('~~ Spawn end: min of max diameters {0:.3f} for medoids: {1}'.format(diam, medoids))

    return diam, medoids


def k_medoids_iterall(points, dists, spawn, diam_max, max_iterations=MAX_ITER, verbose=True):
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

    >>> diam, medoids = k_medoids_iterall(points, diam_max=3, dists=dists, spawn=3)
    * New chosen kernels: [2]
    * Iteration over after 2 steps, max diameter 6
    * New chosen kernels: [6]
    * Iteration over after 2 steps, max diameter 6
    * New chosen kernels: [2]
    * Iteration over after 2 steps, max diameter 6
    ~~ Spawn end: min of max diameters 6.000 for medoids: [Medoid(4, [1, 2, 3, 4, 5, 6, 7])]
    *** Diameter too big 6.000 > 3.000
    *** Now trying 2 clusters

    * New chosen kernels: [6, 2]
    * Iteration over after 2 steps, max diameter 3
    * New chosen kernels: [2, 6]
    * Iteration over after 1 steps, max diameter 3
    * New chosen kernels: [2, 1]
    * Iteration over after 3 steps, max diameter 4
    ~~ Spawn end: min of max diameters 3.000 for medoids: [Medoid(5, [4, 5, 6, 7]), Medoid(2, [1, 2, 3])]
    *** Diameter ok 3.000 <= 3.000
    *** Stopping, 2 clusters enough (7 points initially)
    """
    if not points:
        raise ValueError('No points given!')

    kw = {
        'dists': dists,
        'spawn': spawn,
        'max_iterations': max_iterations,
        'verbose': verbose,
    }

    for k, _ in enumerate(points, start=1):
        diam, medoids = k_medoids_iterspawn(points, k, **kw)
        if diam <= diam_max:
            break

        if verbose:
            print('*** Diameter too big {0:.3f} > {1:.3f}'.format(diam, diam_max))
            print('*** Now trying {0} clusters\n'.format(k + 1))

    if verbose:
        print('*** Diameter ok {0:.3f} <= {1:.3f}'.format(diam, diam_max))
        print('*** Stopping, {0} clusters enough ({1} points initially)'.format(k, len(points)))

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
