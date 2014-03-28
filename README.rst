=======
Medoids
=======

This module handles the clustering, from a general matter.
We have a list of elements and a structure containing their distance,
like dists[p][q] = dists[q][p] = || q - p ||:

.. code-block:: python

    >>> points = [1, 2, 3, 4, 5, 6, 7]
    >>> dists = build_dists(points, custom_dist)
    >>> dists
    {1: {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}, 2: {1: 1,...


Then we have an implementation of the k-medoids algorithm:

.. code-block:: python

    >>> medoids, diam = k_medoids_iterspawn(points, k=2, dists=dists, spawn=2) #doctest: +SKIP
    -- Spawning
    * New chosen kernels: [7, 5]
    * Iteration over after 4 steps
    * Diameter max 3.000 (1, 4) and medoids: {'m1': [2, [1, 2, 3, 4]], 'm0': [6, [5, 6, 7]]}
    -- Spawning
    * New chosen kernels: [1, 6]
    * Iteration over after 2 steps
    * Diameter max 3.000 (4, 7) and medoids: {'m1': [5, [4, 5, 6, 7]], 'm0': [2, [1, 2, 3]]}
    -- Spawn end: best diameter 3.000, best medoids: {'m1': [2, [1, 2, 3, 4]], 'm0': [6, [5, 6, 7]]}
    >>>
    >>> for kernel, medoid in medoids.itervalues():
    ...     print "%s -> %s" % (kernel, medoid) #doctest: +SKIP
    5 -> [4, 5, 6, 7]
    1 -> [1, 2, 3]

And a version which increases automatically the number of clusters till we have homogeneous clusters:

.. code-block:: python

    >>> medoids, diam = k_medoids_iterall(points, diam_max=3, dists=dists, spawn=2) #doctest: +SKIP
    -- Spawning
    * New chosen kernels: [1]
    * Iteration over after 2 steps
    * Diameter max 6.000 (1, 7) and medoids: {'m0': [4, [1, 2, 3, 4, 5, 6, 7]]}
    -- Spawning
    * New chosen kernels: [4]
    * Iteration over after 1 steps
    * Diameter max 6.000 (1, 7) and medoids: {'m0': [4, [1, 2, 3, 4, 5, 6, 7]]}
    -- Spawn end: best diameter 6.000, best medoids: {'m0': [4, [1, 2, 3, 4, 5, 6, 7]]}
    +++ Diameter too bad 6.000 > 3.000
    +++ Going to 2 clusters
    <BLANKLINE>
    -- Spawning
    * New chosen kernels: [7, 5]
    * Iteration over after 4 steps
    * Diameter max 3.000 (1, 4) and medoids: {'m1': [2, [1, 2, 3, 4]], 'm0': [6, [5, 6, 7]]}
    -- Spawning
    * New chosen kernels: [5, 1]
    * Iteration over after 2 steps
    * Diameter max 3.000 (4, 7) and medoids: {'m1': [2, [1, 2, 3]], 'm0': [5, [4, 5, 6, 7]]}
    -- Spawn end: best diameter 3.000, best medoids: {'m1': [2, [1, 2, 3, 4]], 'm0': [6, [5, 6, 7]]}
    +++ Diameter ok 3.000 ~ 3.000
    +++ Stopping, 2 clusters enough (7 points initially)

