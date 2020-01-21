# -*- coding: utf-8 -*-

"""
Test set for superclass Landscape.

This set of tests checks that a landscape object work as expected.

Notes:
     - The classes should pass all tests in this set.
     - The tests check that the class functions work correctly.
"""

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


import random
import pytest
import numpy as np

import biosim.landscape as bl
import biosim.animals as ba


@pytest.fixture(autouse=True)
def reset_parameters():
    """
    Resets all carnivore parameters.
    """
    ba.Herbivore.set_animal_parameters({"w_birth": 8.0, "sigma_birth": 1.5,
                                        "beta": 0.9, "eta": 0.05,
                                        "a_half": 40.0, "phi_age": 0.2,
                                        "w_half": 10.0, "phi_weight": 0.1,
                                        "mu": 0.25, "lambda": 1.0,
                                        "gamma": 0.2, "zeta": 3.5, "xi": 1.2,
                                        "omega": 0.4, "F": 10.0})

    ba.Carnivore.set_animal_parameters({"w_birth": 6.0, "sigma_birth": 1.0,
                                        "beta": 0.75, "eta": 0.125,
                                        "a_half": 60.0, "phi_age": 0.4,
                                        "w_half": 4.0, "phi_weight": 0.4,
                                        "mu": 0.4, "lambda": 1.0, "gamma": 0.8,
                                        "zeta": 3.5, "xi": 1.1, "omega": 0.9,
                                        "F": 50.0, "DeltaPhiMax": 10.0})

    bl.Jungle.set_landscape_parameters({"f_max": 800})
    bl.Savannah.set_landscape_parameters({"f_max": 300,
                                          "alpha": 0.3})

def test_set_landscape_parameters():
    """
    Test that manual setting of landscape parameters works.
    """
    land = bl.Landscape()
    new_parameters = {"f_max": 150}
    land.set_landscape_parameters(new_parameters=new_parameters)
    for key in new_parameters.keys():
        assert new_parameters[key] >= 0


def test_number_of_herbivores():
    """
    Test that the method counts the number of herbivores in the specific cell.
    """
    land = bl.Landscape()
    land.animal_population[0].append(ba.Herbivore())
    assert land.number_of_herbivores == 1


def test_number_of_carnivores():
    """
    Test that the method counts the number of carnivores in the specific cell.
    """
    land = bl.Landscape()
    land.animal_population[1].append(ba.Carnivore())
    assert land.number_of_carnivores == 1


def test_sum_of_herbivore_mass():
    """
    Tests that the sum of herbivore mass is correctly computed.
    """
    land = bl.Landscape()
    pop = [{"species": "Herbivore", "age": 5, "weight": 20}
           for _ in range(100)]
    land.cell_population(pop)
    herb_mass = land.sum_of_herbivore_mass
    assert herb_mass == 2000


def test_cell_population():
    """
    Checks if the cell_population method populates a specific cell with
    the input population.
    """
    land = bl.Landscape()
    pop = [{"species": "Herbivore", "age": 10, "weight": 15},
           {"species": "Herbivore", "age": 5, "weight": 40},
           {"species": "Carnivore", "age": 15, "weight": 25}]
    land.cell_population(population=pop)
    assert land.number_of_herbivores == 2
    assert land.number_of_carnivores == 1


def test_update_fitness():
    """
    Tests if the fitness of animals is updated as expected after weight change.
    """
    land = bl.Landscape()
    land.animal_population[0].append(ba.Herbivore())
    land.animal_population[1].append(ba.Carnivore())
    fit0_herb = land.animal_population[0][0].fitness
    fit0_carn = land.animal_population[1][0].fitness
    land.weight_loss()
    fit1_herb = land.animal_population[0][0].fitness
    fit1_carn = land.animal_population[1][0].fitness
    assert fit0_herb > fit1_herb
    assert fit0_carn > fit1_carn


def test_sort_fitness():
    """
    Tests if sorting of animals based on fitness works correctly.
    """
    land = bl.Landscape()
    pop = [{"species": "Herbivore", "age": 10, "weight": 15},
           {"species": "Herbivore", "age": 5, "weight": 40},
           {"species": "Herbivore", "age": 15, "weight": 25},
           {"species": "Herbivore", "age": 17, "weight": 20},
           {"species": "Herbivore", "age": 8, "weight": 30},
           {"species": "Herbivore", "age": 20, "weight": 35}]
    land.cell_population(population=pop)

    land.sort_by_fitness()

    fit1 = land.animal_population[0][0].fitness
    fit2 = land.animal_population[0][1].fitness
    fit3 = land.animal_population[0][2].fitness
    fit4 = land.animal_population[0][3].fitness
    fit5 = land.animal_population[0][4].fitness
    fit6 = land.animal_population[0][5].fitness

    assert fit1 > fit2
    assert fit2 > fit3
    assert fit4 > fit5
    assert fit5 > fit6


def test_landscape_weight_loss():
    """
    Test that the animal population in a cell has reduced weight following
    a weight-loss occurrence.
    """
    land = bl.Landscape()
    pop = [{"species": "Herbivore", "age": 10, "weight": 15},
           {"species": "Herbivore", "age": 5, "weight": 40},
           {"species": "Carnivore", "age": 10, "weight": 30},
           {"species": "Carnivore", "age": 5, "weight": 20}]
    land.cell_population(pop)
    old_weight = []
    for species in land.animal_population:
        for animal in species:
            old_weight.append(animal.weight)
    land.weight_loss()
    new_weight = []
    for species in land.animal_population:
        for animal in species:
            new_weight.append(animal.weight)
    for index in range(len(old_weight)):
        assert old_weight[index] > new_weight[index]


def test_aging():
    """
    Tests that all animals in a specific specific cell ages by 1 year
    following an aging occurrence.
    """
    land = bl.Landscape()
    pop = [{"species": "Herbivore", "age": 10, "weight": 15},
           {"species": "Herbivore", "age": 5, "weight": 40},
           {"species": "Carnivore", "age": 10, "weight": 30},
           {"species": "Carnivore", "age": 5, "weight": 20},
           {"species": "Carnivore", "age": 18, "weight": 30},
           {"species": "Herbivore", "age": 7, "weight": 50}]
    land.cell_population(pop)
    old_ages = []
    for species in land.animal_population:
        for animal in species:
            old_ages.append(animal.age)
    land.aging()
    new_ages = []
    for species in land.animal_population:
        for animal in species:
            new_ages.append(animal.age)
    for index in range(len(old_ages)):
        assert new_ages[index] == (old_ages[index] + 1)


def test_death():
    """
    Tests that some animals die according to the given formula of probability.
    """
    random.seed(108)
    land = bl.Landscape()
    herbs = [{"species": "Herbivore", "age": 5, "weight": 20}
           for _ in range(1000)]
    carns = [{"species": "Carnivores", "age": 50, "weight": 10}
           for _ in range(1000)]
    pop = herbs + carns
    land.cell_population(pop)
    num_animals = [len(species) for species in land.animal_population]

    land.death()
    num_animals_after_death = [
        len(species) for species in land.animal_population
    ]
    for number in range(len(num_animals)):
        assert num_animals[number] > num_animals_after_death[number]


def test_reproduction():
    """
    Tests that animals in a given cell reproduce according to the provided
    probability function, and add a new animal (a newborn) to the population.
    """

    land = bl.Landscape()
    herbs = [{"species": "Herbivore", "age": 5, "weight": 40}
             for _ in range(1000)]
    carns = [{"species": "Carnivores", "age": 5, "weight": 40}
             for _ in range(1000)]
    pop = herbs + carns
    land.cell_population(pop)
    ini_herbs = len(land.animal_population[0])
    ini_carns = len(land.animal_population[1])
    land.reproduction()
    new_herbs = len(land.animal_population[0])
    new_carns = len(land.animal_population[1])
    assert new_herbs > ini_herbs
    assert new_carns > ini_carns


def test_eat_request_herbivore():
    """
    Test if herbivores eats as expected.
    """
    jungle = bl.Jungle()
    pop = [{"species": "Herbivore", "age": 10, "weight": 15},
     {"species": "Herbivore", "age": 5, "weight": 40},
     {"species": "Herbivore", "age": 10, "weight": 30},
     {"species": "Herbivore", "age": 5, "weight": 20}]
    jungle.cell_population(pop)
    start_weight = jungle.sum_of_herbivore_mass
    jungle.eat_request_herbivore()
    new_weight = jungle.sum_of_herbivore_mass
    assert new_weight > start_weight


def test_eat_request_carnivore():
    """
    Tests that carnivores eat until they are full, and that all herbivores
    that have been eaten are removed from the cells list of
    herbivore population.
    """
    ba.Carnivore.set_animal_parameters({"DeltaPhiMax": 0.0001})
    land = bl.Landscape()
    pop = [{"species": "Herbivore", "age": 10, "weight": 20},
           {"species": "Herbivore", "age": 5, "weight": 20},
           {"species": "Herbivore", "age": 10, "weight": 20},
           {"species": "Carnivore", "age": 5, "weight": 500}]
    land.cell_population(pop)
    land.sort_by_fitness()
    start_weight = land.animal_population[1][0].weight
    land.eat_request_carnivore()
    new_weight = land.animal_population[1][0].weight
    assert len(land.animal_population[0]) == 0
    assert new_weight > start_weight


def test_regenerate():
    """
    Tests that fodder regenerates as expected in the landscape types jungle
    and savannah.
    """
    jungle = bl.Jungle()
    savannah = bl.Savannah()
    landscape_list = [jungle, savannah]
    for landscape in landscape_list:
        landscape.f = 0
        landscape.regenerate()
        assert landscape.f > 0


def test_available_fodder_herbivore():
    """
    Tests that the available fodder for herbivores in a cell is computed
    corresponding to the given formula.
    """
    jungle = bl.Jungle()
    herbs = [{"species": "Herbivore", "age": 5, "weight": 40}
             for _ in range(4)]
    jungle.cell_population(herbs)

    assert jungle.available_fodder_herbivore == 16
    jungle.eat_request_herbivore()
    assert jungle.available_fodder_herbivore == pytest.approx(15.2)


def test_available_fodder_carnivore():
    """
    Tests that the available fodder for carnivores in a cell is computed
    corresponding to the given formula.
    """
    jungle = bl.Jungle()
    herbs = [{"species": "Herbivore", "age": 5, "weight": 50}
             for _ in range(4)]
    ba.Carnivore.set_animal_parameters({"DeltaPhiMax": 0.0001})
    carn = [{"species": "Carnivore", "age": 5, "weight": 500}
            for _ in range(2)]
    pop = herbs + carn
    jungle.cell_population(pop)
    assert jungle.available_fodder_carnivore == pytest.approx(1.3333333)
    jungle.eat_request_carnivore()
    assert jungle.available_fodder_carnivore == pytest.approx(0.666666, 2)


def test_propensity_herbivore():
    """
    Tests that the propensity function for herbivores works.
    """
    jungle = bl.Jungle()
    assert jungle.propensity()[0] == pytest.approx(np.exp(80))

    savannah = bl.Savannah()
    assert savannah.propensity()[0] == pytest.approx(np.exp(30))

    desert = bl.Desert()
    assert desert.propensity()[0] == 1

    mountain = bl.Mountain()
    ocean = bl.Ocean()
    uninhabitable_landscapes = [mountain, ocean]
    for landscape in uninhabitable_landscapes:
        assert landscape.propensity()[0] == 0


def test_propensity_carnivore():
    """
    Tests that the propensity function for carnivores works.
    """
    herbs = [{"species": "Herbivore", "age": 5, "weight": 50}
             for _ in range(4)]

    jungle = bl.Jungle()
    jungle.cell_population(herbs)
    assert jungle.propensity()[1] == pytest.approx(np.exp(4))

    savannah = bl.Savannah()
    savannah.cell_population(herbs)
    savannah.animal_population[0].append(ba.Herbivore(weight=25))
    assert savannah.propensity()[1] == pytest.approx(np.exp(4.5),
                                                     rel=1e-1)

    desert = bl.Desert()
    desert.cell_population(herbs)
    desert.animal_population[0].append(ba.Herbivore(weight=68))
    assert desert.propensity()[1] == pytest.approx(np.exp(5.36),
                                                   rel=1e-1)

    mountain = bl.Mountain()
    ocean = bl.Ocean()
    uninhabitable_landscapes = [mountain, ocean]
    for landscape in uninhabitable_landscapes:
        landscape.cell_population(herbs)
        assert landscape.propensity()[0] == 0


def test_directional_probability():
    """
    Tests that the probabilities of moving to the adjacent cells are computed
    correctly.
    """
    current_cell_pop = [{"species": "Herbivore", "age": 10, "weight": 15},
           {"species": "Carnivore", "age": 5, "weight": 40},
           {"species": "Carnivore", "age": 15, "weight": 25}]
    current_cell = bl.Jungle()
    current_cell.cell_population(current_cell_pop)
    jungle_right = bl.Jungle()
    jungle_left = bl.Jungle()
    desert = bl.Desert()
    jungle_right.animal_population[0].append(ba.Herbivore(weight=15))
    jungle_pop = [{"species": "Herbivore", "age": 10, "weight": 15},
                  {"species": "Herbivore", "age": 5, "weight": 15}]
    jungle_left.cell_population(jungle_pop)
    desert_pop = [{"species": "Herbivore", "age": 10, "weight": 20},
                  {"species": "Herbivore", "age": 5, "weight": 15},
                  {"species": "Herbivore", "age": 10, "weight": 35}]
    desert.cell_population(desert_pop)

    neighbour_cells = [desert, bl.Mountain(), jungle_right, jungle_left]

    herbivore_probabilities = current_cell.directional_probability(
        current_cell.animal_population[0][0], neighbour_cells)
    carnivore_probabilities = current_cell.directional_probability(
        current_cell.animal_population[1][0], neighbour_cells)

    assert herbivore_probabilities != carnivore_probabilities
    # The numbers below are calculated manually.
    assert carnivore_probabilities == pytest.approx([0.56, 0.0, 0.18, 0.25],
                                                    rel=1e-1)


def test_choose_migration_cell(mocker):
    """
    Tests whether animals are migrating to the correct cell, given the animals
    probability to move to a specific cell.
    """
    current_cell = bl.Desert()
    current_cell.animal_population[0].append(ba.Herbivore())
    desert = bl.Desert()
    jungle = bl.Jungle()
    savannah = bl.Savannah()
    neighbour_cells = [desert, bl.Mountain(), jungle, savannah]
    probability_list = [0.25, 0.0, 0.5, 0.25]
    mocker.patch("random.random", return_value=0.7)
    current_cell.choose_migration_cell(current_cell.animal_population[0][0],
                                       neighbour_cells, probability_list)
    assert len(current_cell.new_population[0]) == 0
    assert len(jungle.new_population[0]) == 1


def test_migrate():
    """
    Tests that migration of animals work as expected.
    """
    current_cell_pop = [{"species": "Herbivore", "age": 10, "weight": 15},
                        {"species": "Herbivore", "age": 20, "weight": 35},
                        {"species": "Carnivore", "age": 5, "weight": 40},
                        {"species": "Carnivore", "age": 15, "weight": 25}]
    current_cell = bl.Savannah()
    current_cell.cell_population(current_cell_pop)
    jungle_right = bl.Jungle()
    jungle_left = bl.Jungle()
    desert = bl.Desert()
    jungle_right.animal_population[0].append(ba.Herbivore(weight=15))
    jungle_pop = [{"species": "Herbivore", "age": 10, "weight": 15},
                  {"species": "Herbivore", "age": 5, "weight": 15}]
    jungle_left.cell_population(jungle_pop)
    desert_pop = [{"species": "Herbivore", "age": 10, "weight": 20},
                  {"species": "Herbivore", "age": 5, "weight": 15},
                  {"species": "Herbivore", "age": 10, "weight": 35}]
    desert.cell_population(desert_pop)

    neighbour_cells = [desert, bl.Mountain(), jungle_right, jungle_left]

    random.seed(124)
    current_cell.migrate(neighbour_cells)

    neighbour_cells.append(current_cell)
    for cell in neighbour_cells:
        if not isinstance(cell, bl.Mountain):
            assert cell.new_population != cell.animal_population


def test_update_cell_population(mocker):
    """
    Tests whether the cells animal population is updated after a migration
    cycle.
    """
    current_cell = bl.Desert()
    current_cell.animal_population[0].append(ba.Herbivore())
    desert = bl.Desert()
    jungle = bl.Jungle()
    savannah = bl.Savannah()

    neighbour_cells = [desert, bl.Mountain(), jungle, savannah]
    probability_list = [0.25, 0.0, 0.5, 0.25]
    mocker.patch("random.random", return_value=0.7)

    current_cell_old_population = current_cell.animal_population
    jungle_cell_old_population = jungle.animal_population

    current_cell.choose_migration_cell(current_cell.animal_population[0][0],
                                       neighbour_cells, probability_list)

    neighbour_cells.append(current_cell)
    for cell in neighbour_cells:
        cell.update_cell_population()

    current_cell_new_population = current_cell.animal_population
    jungle_cell_new_population = jungle.animal_population

    assert current_cell_new_population != current_cell_old_population
    assert jungle_cell_new_population != jungle_cell_old_population
