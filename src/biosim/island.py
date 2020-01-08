# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad, Håvard Molversmyr"
__email__ = "erikrull@nmbu.no, havardmo@nmbu.no"


class Island:
    """
    This class generates the island nation of Pylandia.
    """
    def __init__(self):
        """
        This method creates variables needed for the class.
        """
        pass

    def map_of_pylandia(self, input_map=None):
        """
        This method creates the map.
        :param input_map: map represented as a multi line string.
        :return:
        """
        standard_map = """\
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
        if input_map is None:
            island_map = standard_map
        else:
            island_map = input_map
