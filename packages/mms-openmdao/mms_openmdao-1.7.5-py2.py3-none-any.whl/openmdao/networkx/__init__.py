"""
NetworkX
========

    NetworkX (NX) is a Python package for the creation, manipulation, and
    study of the structure, dynamics, and functions of complex networks.

    https://networkx.lanl.gov/

Using
-----

    Just write in Python

    >>> import openmdao.networkx as nx
    >>> G=nx.Graph()
    >>> G.add_edge(1,2)
    >>> G.add_node(42)
    >>> print(sorted(G.nodes()))
    [1, 2, 42]
    >>> print(sorted(G.edges()))
    [(1, 2)]
"""
#    Copyright (C) 2004-2015 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Add platform dependent shared library path to sys.path
#

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 7):
    m = "Python 2.7 or later is required for NetworkX (%d.%d detected)."
    raise ImportError(m % sys.version_info[:2])
del sys

# Release data
from openmdao.networkx import release

__author__ = '%s <%s>\n%s <%s>\n%s <%s>' % \
    (release.authors['Hagberg'] + release.authors['Schult'] +
        release.authors['Swart'])
__license__ = release.license

__date__ = release.date
__version__ = release.version

__bibtex__ = """@inproceedings{hagberg-2008-exploring,
author = {Aric A. Hagberg and Daniel A. Schult and Pieter J. Swart},
title = {Exploring network structure, dynamics, and function using {NetworkX}},
year = {2008},
month = Aug,
urlpdf = {http://math.lanl.gov/~hagberg/Papers/hagberg-2008-exploring.pdf},
booktitle = {Proceedings of the 7th Python in Science Conference (SciPy2008)},
editors = {G\"{a}el Varoquaux, Travis Vaught, and Jarrod Millman},
address = {Pasadena, CA USA},
pages = {11--15}
}"""

# These are import orderwise
from openmdao.networkx.exception import *
import openmdao.networkx.external
import openmdao.networkx.utils

import openmdao.networkx.classes
from openmdao.networkx.classes import *


import openmdao.networkx.convert
from openmdao.networkx.convert import *

import openmdao.networkx.convert_matrix
from openmdao.networkx.convert_matrix import *


import openmdao.networkx.relabel
from openmdao.networkx.relabel import *

import openmdao.networkx.generators
from openmdao.networkx.generators import *

import openmdao.networkx.readwrite
from openmdao.networkx.readwrite import *

# Need to test with SciPy, when available
import openmdao.networkx.algorithms
from openmdao.networkx.algorithms import *
import openmdao.networkx.linalg

from openmdao.networkx.linalg import *
# from openmdao.networkx.tests.test import run as test

import openmdao.networkx.drawing
from openmdao.networkx.drawing import *
