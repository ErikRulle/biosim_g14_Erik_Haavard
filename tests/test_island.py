# -*- coding: utf-8 -*-

"""
Test set for class Island.

This set of tests checks that the island class work as expected.

Notes:
     - The class should pass all tests in this set.
     - The tests check that the class functions work correctly.
"""

__author__ = "Erik Rullestad, Håvard Molversmyr"
__email__ = "erikrull@nmbu.no, havardmo@nmbu.no"


import numpy as np

import examples.population_generator as pg
import biosim.island as bi
import biosim.landscape as bl


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
    island_map = """\
                    OOOOOOO
                    OSSSSSO
                    OSJJJSO
                    OSJMJSO
                    OSJDJSO
                    OSJJJSO
                    OSSSSSO
                    OOOOOOO"""

    island = bi.Island(island_map)
    assert isinstance(island.numpy_map, np.ndarray)
    assert isinstance(island.numpy_map[0][0], bl.Ocean)
    assert isinstance(island.numpy_map[3][3], bl.Mountain)
    assert isinstance(island.numpy_map[4][3], bl.Desert)
    assert isinstance(island.numpy_map[3][2], bl.Jungle)
    assert isinstance(island.numpy_map[4][5], bl.Savannah)


def test_find_cell_position():
    """
    Tests if the function find correct cell positions.
    """
    island = bi.Island()
    positions = []
    for cell in island.numpy_map[0][0:5]:
        positions.append(island.find_cell_position(cell))

    true_positions = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    assert positions == true_positions


def test_find_surrounding_cells():
    """
    Tests if the function finds the wanted neighbouring cells for a
    specific cell.
    """
    island_map = """\
                       OOOO
                       ODOO
                       OSJO
                       OMOO
                       OOOO"""
    island = bi.Island(island_map)
    neighbour_cells = island.find_surrounding_cells([2, 1])
    assert isinstance(neighbour_cells[0], bl.Mountain)
    assert isinstance(neighbour_cells[1], bl.Desert)
    assert isinstance(neighbour_cells[2], bl.Jungle)
    assert isinstance(neighbour_cells[3], bl.Ocean)


def test_populate_the_island():
    """
    Tests that the function puts an animal population in the wanted cells.
    """
    island_map = """\
                        OOOOOOO
                        OSSSSSO
                        OSJJJSO
                        OSJMJSO
                        OSDDJSO
                        OSJJJSO
                        OSSSSSO
                        OOOOOOO"""

    island = bi.Island(island_map)
    popgen = pg.Population(n_herbivores=3,
                           coord_herb=[(5, 2), (2, 5), (4, 3)])
    pop = popgen.get_animals()
    island.populate_the_island(pop)
    assert len(island.numpy_map[5][2].animal_population[0]) == 3
    assert isinstance(island.numpy_map[5][2], bl.Jungle)
    assert len(island.numpy_map[2][5].animal_population[0]) == 3
    assert isinstance(island.numpy_map[2][5], bl.Savannah)
    assert len(island.numpy_map[4][3].animal_population[0]) == 3
    assert isinstance(island.numpy_map[4][3], bl.Desert)


def test_population_in_each_cell():
    """
    Tests if the function counts the population in each cell correctly.
    """
    island_map = """\
                            OOOOOOO
                            OSSSSSO
                            OSJJJSO
                            OSJMJSO
                            OSDDJSO
                            OSJJJSO
                            OSSSSSO
                            OOOOOOO"""

    island = bi.Island(island_map)
    popgen = pg.Population(n_herbivores=3,
                           coord_herb=[(5, 2), (2, 5), (4, 3)],
                           n_carnivores=2, coord_carn=[(5, 3), (1, 5)])
    pop = popgen.get_animals()
    island.populate_the_island(pop)
    cell_populations = island.population_in_each_cell
    assert cell_populations[19][2] == 3
    assert cell_populations[37][2] == 3
    assert cell_populations[31][2] == 3
    assert cell_populations[12][3] == 2
    assert cell_populations[38][3] == 2
    assert cell_populations[36].all() == 0


def test_total_population():
    """
    Tests if the function can find the correct herbivore, carnivore and
    total animal population of the island.
    """
    island_map = """\
                                OOOOOOO
                                OSSSSSO
                                OSJJJSO
                                OSJMJSO
                                OSDDJSO
                                OSJJJSO
                                OSSSSSO
                                OOOOOOO"""

    island = bi.Island(island_map)
    popgen = pg.Population(n_herbivores=3,
                           coord_herb=[(5, 2), (2, 5), (4, 3)],
                           n_carnivores=2, coord_carn=[(5, 3), (1, 5)])
    pop = popgen.get_animals()
    island.populate_the_island(pop)
    species_population = island.total_species_population
    total_population = island.total_island_population
    assert species_population == (9, 4)
    assert total_population == 13


# def test_annual_cycle():
#     import matplotlib.pyplot as plt
#     island_map = """\
#                      OOOOOO
#                      OJSSDO
#                      OSJJMO
#                      OOOOOO"""
#     island = bi.Island(island_map)
#
#     popgen = pg.Population(n_herbivores=3,
#                            coord_herb=[(1, 1), (1, 1), (2, 1)],
#                            n_carnivores=5, coord_carn=[(1, 1), (2, 1)])
#     pop = popgen.get_animals()
#     island.populate_the_island(pop)
#     herbivore_list = [island.total_island_population[0]]
#     carnivore_list = [island.total_island_population[1]]
#     for year in range(100):
#         new_island_population = island.annual_cycle()
#         herbivore_list.append(new_island_population[0])
#         carnivore_list.append(new_island_population[1])
#         plt.plot(range(len(herbivore_list)), herbivore_list)
#         plt.plot(range(len(carnivore_list)), carnivore_list)
#         plt.legend(["Herbivores", "Carnivores"], loc="upper left")
#         #plt.show()
        #plt.savefig()




def test_animals_in_island():
    island_map = "OOOO\nOJSO\nOOOO"
    ini_pop = []
    island = bi.Island(island_map)
    island.populate_the_island(ini_pop)
    assert island.total_island_population == 0