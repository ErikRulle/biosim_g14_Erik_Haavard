# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


from biosim.landscape import *


def test_set_landscape_parameters():
    """
    Test that manual setting of landscape parameters works.
    """
    land = Landscape()
    new_parameters = {"f_max": 150}
    land.set_landscape_parameters(new_parameters=new_parameters)
    for key in new_parameters.keys():
        assert new_parameters[key] >= 0


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


def test_sum_of_herbivore_mass():
    land = Landscape()
    pop = [{'species': 'Herbivore', 'age': 5, 'weight': 20}
           for _ in range(100)]
    land.cell_population(pop)
    herb_mass = land.sum_of_herbivore_mass
    assert herb_mass == 2000


def test_cell_population():
    """
    Checks if the cell_population method populates a specific cell with
    the input population.
    """
    land = Landscape()
    pop = [{"species": "Herbivore", "age": 10, "weight": 15},
           {"species": "Herbivore", "age": 5, "weight": 40},
           {"species": "Carnivore", "age": 15, "weight": 25}]
    land.cell_population(population=pop)
    assert land.number_of_herbivores == 2
    assert land.number_of_carnivores == 1


def test_update_fitness():
    land = Landscape()
    land.animal_population[0].append(Herbivore())
    land.animal_population[1].append(Carnivore())
    fit0_herb = land.animal_population[0][0].fitness
    fit0_carn = land.animal_population[1][0].phi
    land.weight_loss()
    fit1_herb = land.animal_population[0][0].fitness
    fit1_carn = land.animal_population[1][0].phi
    assert fit0_herb > fit1_herb
    assert fit0_carn > fit1_carn


def test_sort_fitness():
    land = Landscape()
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
    a weight-loss occurence.
    """
    land = Landscape()
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
    following an aging occurence.
    """
    land = Landscape()
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
    random.seed(1093)
    land = Landscape()
    herbs = [{'species': 'Herbivore', 'age': 5, 'weight': 20}
           for _ in range(1000)]
    carns = [{'species': 'Carnivores', 'age': 5, 'weight': 20}
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

    land = Landscape()
    herbs = [{'species': 'Herbivore', 'age': 5, 'weight': 40}
             for _ in range(1000)]
    carns = [{'species': 'Carnivores', 'age': 5, 'weight': 40}
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
    jungle = Jungle()
    pop = [{"species": "Herbivore", "age": 10, "weight": 15},
     {"species": "Herbivore", "age": 5, "weight": 40},
     {"species": "Herbivore", "age": 10, "weight": 30},
     {"species": "Herbivore", "age": 5, "weight": 20}]
    jungle.cell_population(pop)
    start_weight = jungle.sum_of_herbivore_mass
    jungle.eat_request_herbivore
    new_weight = jungle.sum_of_herbivore_mass
    assert new_weight > start_weight











