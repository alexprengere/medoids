=======
Medoids
=======

This module handles the clustering, from a general matter.
We have a list of elements and a structure containing their distance,
like ``dists[p][q] = dists[q][p] = || q - p ||``:

.. code-block:: python

    >>> from medoids import build_distances
    >>> points = [1, 2, 3, 4, 5, 6, 7]
    >>> dists = build_distances(points, lambda a, b:  abs(b - a))
    >>> dists
    {1: {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}, 2: {1: 1, ...

We just import the main functions.

.. code-block:: python

    >>> from medoids import k_medoids_iterspawn, k_medoids_iterall

Then we have an implementation of the k-medoids algorithm:

.. code-block:: python

    >>> medoids, diam = k_medoids_iterspawn(points, k=2, dists=dists, spawn=2) #doctest: +SKIP
    * New chosen kernels: [1, 2]
    * Iteration over after 4 steps
    * New chosen kernels: [6, 4]
    * Iteration over after 3 steps
    -- Spawn end: best diameter 3.000, best medoids: [Medoid(2, [1, 2, 3]), Medoid(5, [4, 5, 6, 7])]

And a version which increases automatically the number of clusters till we have homogeneous clusters:

.. code-block:: python

    >>> medoids, diam = k_medoids_iterall(points, diam_max=3, dists=dists, spawn=2) #doctest: +SKIP
    * New chosen kernels: [2]
    * Iteration over after 2 steps
    * New chosen kernels: [1]
    * Iteration over after 2 steps
    -- Spawn end: best diameter 6.000, best medoids: [Medoid(4, [1, 2, 3, 4, 5, 6, 7])]
    +++ Diameter too bad 6.000 > 3.000
    +++ Going to 2 clusters

    * New chosen kernels: [6, 7]
    * Iteration over after 4 steps
    * New chosen kernels: [2, 3]
    * Iteration over after 3 steps
    -- Spawn end: best diameter 3.000, best medoids: [Medoid(2, [1, 2, 3, 4]), Medoid(6, [5, 6, 7])]
    +++ Diameter ok 3.000 ~ 3.000
    +++ Stopping, 2 clusters enough (7 points initially)

