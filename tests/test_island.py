# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad, Håvard Molversmyr"
__email__ = "erikrull@nmbu.no, havardmo@nmbu.no"

from biosim.island import *


def test_island_instance():
    """

    """
    island = Island()
    assert isinstance(island, Island)

def test_landscape_position_in_map():
    """

    :return:
    """
    island = Island()
    island.landscape_position_in_map()
    assert isinstance(island.numpy_map, numpy.ndarray)



