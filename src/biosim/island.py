# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad, Håvard Molversmyr"
__email__ = "erikrull@nmbu.no, havardmo@nmbu.no"


class Island:
    """
    This class generates the island nation of Pylandia.
    """

    STANDARD_MAP = """\
                       OOOOOOOOOOOOOOOOOOOOO
                       OOOOOOOOSMMMMJJJJJJJO
                       OSSSSSJJJJMMJJJJJJJOO
                       OSSSSSSSSSMMJJJJJJOOO
                       OSSSSSJJJJJJJJJJJJOOO
                       OSSSSSJJJDDJJJSJJJOOO
                       OSSJJJJJDDDJJJSSSSOOO
                       OOSSSSJJJDDJJJSOOOOOO
                       OSSSJJJJJDDJJJJJJJOOO
                       OSSSSJJJJDDJJJJOOOOOO
                       OOSSSSJJJJJJJJOOOOOOO
                       OOOSSSSJJJJJJJOOOOOOO
                       OOOOOOOOOOOOOOOOOOOOO"""

    def __init__(self, island_map=None):
        """
        This method creates variables needed for the class.
        """

        if island_map is None:
            self.island_map = self.STANDARD_MAP
        else:
            self.island_map = island_map

        self.validate_map_string(self.island_map)


    def validate_map_string(self, island_map):
        string_map = island_map.replace(" ", "").splitlines()
        accepted_landscape_types = ["J", "S", "D", "M", "O"]
        for row in string_map:
            for cell in row:
                if cell not in accepted_landscape_types:
                    raise ValueError(
                        "You have entered invalid landscape types.\n"
                        "Please enter the following landscape types:\n"
                        "J = Jungle\n"
                        "S = Savannah\n"
                        "D = Desert\n"
                        "M = Mountain\n"
                        "O = Ocean\n")

        error_message = ValueError("The edges of the map has to be Ocean")
        for end in [0, -1]:
            for cell in string_map[end]:
                if cell != "O":
                    raise error_message
        for row in string_map[1:-1]:
            first_cell = row.startswith("O")
            last_cell = row.endswith("O")
            if not (first_cell and last_cell):
                raise error_message

        row_lengths = [len(row) for row in string_map]
        for length in row_lengths:
            if length != row_lengths[0]:
                raise ValueError("All rows of the map must be of same length")

