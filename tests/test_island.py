# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad, Håvard Molversmyr"
__email__ = "erikrull@nmbu.no, havardmo@nmbu.no"

from island import *

def test_island_instance():
    """

    """
    island = Island()
    assert isinstance(island, Island)

def test_map_string(island_map):
    string_map = island_map.replace(" ", "").splitlines()
    accepted_landscape_types = ["J", "S", "D", "M", "O"]
    for row in string_map:
        for cell in row:
            if cell not in accepted_landscape_types:
                raise ValueError("You have entered invalid landscape types,"
                                 "please enter the following landscape types:"
                                 "J=Jungle"
                                 "S=Savannah"
                                 "D=Desert"
                                 "M=Mountain"
                                 "O=Ocean")

    error_message = ValueError("The edges of the map has to be Ocean")
    for end in [0, -1]:
        for cell in string_map[end]:
            if cell != "O":
                raise error_message
    for row in string_map[1:-1]:
        first_cell = row.startswith("O")
        last_cell = row.endswith("O")
        if not first_cell and last_cell:
            raise error_message

    row_lengths = [len(row) for row in string_map]
    for length in row_lengths:
        assert length == len(string_map[0])




