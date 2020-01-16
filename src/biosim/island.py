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
        Validates that a the input map string follows the constraints of the
        model.
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

        :return: numpy_map, numpy.ndarray map with landscape positions
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
        Collects a cell's neighbouring landscape types.

        :param position: tuple (cell coordinates)
        :return neighbour_cells: list, objects of adjacent cells
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

    def annual_cycle(self):
        """
        This method carries out one cycle on the island.
        :return:
        """
        for row in self.numpy_map:
            for cell in row:
                if callable(getattr(cell, "regenerate", None)):
                    cell.regenerate()
                else:
                    pass
                cell.sort_by_fitness()
                cell.eat_request_herbivore()
                cell.eat_request_carnivore()
                cell.update_fitness()
                cell.reproduction()
                cell.migrate()
                cell.update_cell_population()
                cell.aging()
                cell.weight_loss()
                cell.update_fitness()
                cell.death()

            return self.total_island_population

    @property
    def population_in_each_cell(self):
        """
        This method calculates the herbivore and carnivore population for
        each cell.
        :return: numpy.ndarray, the herbivore and carnivore population in the
                 first and second element of each list, respectively
        """
        number_of_herbivores = []
        number_of_carnivores = []

        for row in self.map:
            for cell in row:
                number_of_herbivores.append(len(cell.animal_population[0]))
                number_of_carnivores.append(len(cell.animal_population[1]))
        return np.column_stack((number_of_herbivores, number_of_carnivores))

    @property
    def total_island_population(self):
        """
        Finds the total number of herbivores and carnivores on the island.
        :return: tuple
        """
        population = self.population_in_each_cell
        herbivores = [population[i][0] for i in range(len(population))]
        carnivores = [population[i][1] for i in range(len(population))]

        return sum(herbivores), sum(carnivores)

    def assign_animals_to_cell(self, start_population=None):
        """

        """
        start_herbivore_population = [{"loc": (10, 10),
                      "pop": [{"species": "Herbivore", "age": 5,
                               "weight": 20} for _ in range(150)]}]
        start_carnivore_population = [{"loc": (10, 10),
                      "pop": [{"species": "Carnivore", "age": 5,
                               "weight": 20} for _ in range(40)]}]
        standard_pop = start_herbivore_population + start_carnivore_population

        if not start_population:
            population = standard_pop
        else:
            population = start_population

        for dictionary in population:
            map_row = dictionary["loc"][0]
            map_col = dictionary["loc"][1]

            if not 0 <= map_row <= self.numpy_map.shape[0]:
                raise ValueError("This x-value is not valid, "
                                 "please enter a value between 0 and " +
                                 str(self.numpy_map.shape[0]))

            elif not 0 <= map_col <= self.numpy_map.shape[1]:
                raise ValueError("This y-value is not valid, "
                                 "please enter a value between 0 and " +
                                 str(self.numpy_map.shape[1]))

            cell = self.numpy_map[(map_row - 1, map_col - 1)]

            if isinstance(cell, (bl.Mountain, bl.Ocean)):
                raise ValueError("Animals can not stay in " +
                                 str(type(cell)).split(
                                     sep="'")[1].split(sep=".")[-1] +
                                 ". Allowed landscapes: Jungle, Savannah"
                                 " and Desert.")
            for animal in dictionary["pop"]:
                age, weight = animal["age"], animal["weight"]
                if not isinstance(age, int) or age < 0 or weight < 0:
                    raise ValueError("Violated one/both of two conditions:\n"
                                     "1. Animal age has to be a non-negative"
                                     " integer.\n2. Animal weight has to be"
                                     " a non-negative number(float).")

            cell.cell_population(dictionary["pop"])

    def populate_the_island(self, start_population=None):
        """

        :return:
        """
        self.numpy_map = self.landscape_position_in_map()
        self.assign_animals_to_cell(start_population)