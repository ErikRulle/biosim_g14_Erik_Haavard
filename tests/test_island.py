# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad, Håvard Molversmyr"
__email__ = "erikrull@nmbu.no, havardmo@nmbu.no"

import numpy as np
import biosim.island as bi


def test_island_instance():
    """
    Tests whether an Island instance can be created.
    """
    island = bi.Island()
    assert isinstance(island, bi.Island)


def test_landscape_position_in_map():
    """
    Tests that a numpy array is created from the method.
    """
    island = bi.Island()
    island.landscape_position_in_map()
    assert isinstance(island.numpy_map, np.ndarray)
