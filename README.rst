=========
K-Medoids
=========

This module implements a K-medoids algorithm using as input a list of points
and a distance function, like ``distance(p, q) = ||q - p||``:

.. code-block:: python

    >>> points = [1, 2, 3, 4, 5, 6, 7]
    >>> distance = lambda a, b: abs(b - a)

Just import the main ``k_medoids`` function:

.. code-block:: python

    >>> from medoids import k_medoids
    >>> diameter, medoids = k_medoids(points, k=2, distance, spawn=2) #doctest: +SKIP
    * New chosen kernels: [2, 3]
    * Iteration over after 3 steps, max diameter 3
    * New chosen kernels: [1, 2]
    * Iteration over after 4 steps, max diameter 3
    ~~ Spawn end: min of max diameters 3.000 for medoids: [Medoid(2, [1, 2, 3]), Medoid(5, [4, 5, 6, 7])]

There is also a ``k_medoids_auto_k`` which increases automatically the number of clusters
until we have homogeneous clusters:

.. code-block:: python

    >>> from medoids import k_medoids_auto_k
    >>> diameter, medoids = k_medoids_auto_k(points, diam_max=3, distance, spawn=3) #doctest: +SKIP
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
