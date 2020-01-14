# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad, Håvard Molversmyr"
__email__ = "erikrull@nmbu.no, havardmo@nmbu.no"


import biosim.landscape as bl
import numpy as np
import random


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

        self.string_map = self.island_map.replace(" ", "").splitlines()
        self.validate_map_string()
        self.numpy_map = None

    def validate_map_string(self):
        """

        """
        accepted_landscape_types = ["J", "S", "D", "M", "O"]
        for row in self.string_map:
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
            for cell in self.string_map[end]:
                if cell != "O":
                    raise error_message
        for row in self.string_map[1:-1]:
            first_cell = row.startswith("O")
            last_cell = row.endswith("O")
            if not (first_cell and last_cell):
                raise error_message

        row_lengths = [len(row) for row in self.string_map]
        for length in row_lengths:
            if length != row_lengths[0]:
                raise ValueError("All rows of the map must be of same length")

    def landscape_position_in_map(self):
        """
        Creates the numpy array map

        :return: numpy.ndarray, numpy map with landscape positions
        """
        self.numpy_map = np.empty(
            (len(self.string_map), len(self.string_map[0])), dtype=object)
        for x, line in enumerate(self.string_map):
            for y, cell in enumerate(line):
                if cell == "J":
                    self.numpy_map[x, y] = bl.Jungle()
                elif cell == "S":
                    self.numpy_map[x, y] = bl.Savannah()
                elif cell == "D":
                    self.numpy_map[x, y] = bl.Desert()
                elif cell == "M":
                    self.numpy_map[x, y] = bl.Mountain()
                elif cell == "O":
                    self.numpy_map[x, y] = bl.Ocean()
        return self.numpy_map

    def possible_migration_cells(self, position):
        """
        Collects a cell's neighbouring cells
        Returns a list of valid cells for migration

        :param position: tuple (cell coordinates)
        :return neighbour_cells: list
        """
        neighbour_cells = []
        x, y = position
        if x + 1 < len(self.numpy_map):
            neighbour_cells.append(self.numpy_map[x + 1, y])
        if x - 1 >= 0:
            neighbour_cells.append(self.numpy_map[x - 1, y])
        if y + 1 < len(self.numpy_map[0]):
            neighbour_cells.append(self.numpy_map[x, y + 1])
        if y - 1 >= 0:
            neighbour_cells.append(self.numpy_map[x, y - 1])
        return neighbour_cells

    def directional_probability_herbivore(self, neighbour_cells):
        """
        This method estimates the propensity for each neighbouring cell, and
        calculates the probability of herbivores migrating to that cell.
        Stores the result in a list.

        :param neighbour_cells:
        :return probability_list: list of probabilities
        """
        propensities = [cell.propensity_herbivore()
                        for cell in neighbour_cells]
        probability_list = [propensity / sum(propensities)
                            for propensity in propensities]
        return probability_list

    def directional_probability_carnivore(self, neighbour_cells):
        """
        This method estimates the propensity for each neighbouring cell, and
        calculates the probability of carnivores migrating to that cell.
        Stores the result in a list.

        :param neighbour_cells:
        :return probability_list: list of probabilities
        """
        propensities = [cell.propensity_carnivore()
                        for cell in neighbour_cells]
        probability_list = [propensity / sum(propensities)
                            for propensity in propensities]
        return probability_list

    def island_migration(self, probability_list, neighbour_cells):
        """

        :param probability_list:
        :param neighbour_cells:
        """

        p = random.random()
        i = 0
        while p > sum(probability_list[0:i]):
            i += 1
        return neighbour_cells[i - 1].new_population[0]
