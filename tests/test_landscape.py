# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


def test_number_of_herbivores():
    """
    Test that the method counts the number of herbivores in the specific cell.
    """
    land = Landscape()
    land.animal_population[0].append(Herbivore())
    assert land.number_of_herbivores == 1

def test_number_of_carnivores():
    """
    Test that the method counts the number of carnivores in the specific cell.
    """
    land = Landscape()
    land.animal_population[1].append(Carnivore())
    assert land.number_of_carnivores == 1

def test_cell_population():
    """
    Checks if the cell_population method populates a specific cell with
    the input population.
    """
    land = Landscape()
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 15},
           {'species': 'Herbivore', 'age': 5, 'weight': 40},
           {'species': 'Carnivore', 'age': 15, 'weight': 25}]
    land.cell_population(population=pop)
    assert land.number_of_herbivores == 2
    assert land.number_of_carnivores == 1

def test_sort_by_fitness():
    land = Landscape()
    land.animal_population[0].append(Herbivore())
    land.animal_population[1].append(Carnivore())
    fit0_herb = land.animal_population[0][0].phi
    fit0_carn = land.animal_population[1][0].phi
    land.weight_loss()
    fit1_herb = land.animal_population[0][0].phi
    fit1_carn = land.animal_population[1][0].phi
    assert fit0_herb > fit1_herb
    assert fit0_carn > fit1_carn 


