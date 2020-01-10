# -*- coding: utf-8 -*-

"""
Test set for superclass Animals, and subclasses Herbivores and Carnivores.

Test set for Animal class along with the subclasses Herbivores and Carnivores.

This set of tests checks the interface of the BioSim class to be provided by
the simulation module of the biosim package.

Notes:
     - The classes should pass all tests in this set.
     - The tests check only that the class interface can be used, not that
       the class functions correctly. You need to write your own tests for that.
     - You should only run these tests on your code *after* you have implemented
       both animal and all landscape classes.
"""

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


from biosim.animals import *
from pytest import approx


def test_herbivore_parameters():
    """
    Tests that the given parameters for the herbivore class are in the list
     of valid parameters.
    """
    keys_list = ['w_birth', 'sigma_birth', 'beta','eta', 'a_half', 'phi_age',
                 'w_half', 'phi_weight', 'mu', 'lambda', 'gamma',  'zeta',
                 'xi', 'omega', 'F']
    herb = Herbivore()
    for key in keys_list:
        assert key in herb.default_parameters.keys()


def test_carnivore_parameters():
    """
    Tests that the given parameters for the carnivore class are in the list
     of valid parameters.
    """
    keys_list = ['w_birth', 'sigma_birth', 'beta', 'eta', 'a_half', 'phi_age',
                 'w_half', 'phi_weight', 'mu', 'lambda', 'gamma', 'zeta',
                 'xi', 'omega', 'F', 'DeltaPhiMax']
    carn = Carnivore()
    for key in keys_list:
        assert key in carn.default_parameters.keys()


def test_non_negative_animal_weight():
    """Tests that animals has a non-negative weight."""
    herb = Herbivore()
    carn = Carnivore()
    assert isinstance(herb, Herbivore)
    assert herb.weight >= 0
    assert isinstance(carn, Carnivore)
    assert carn.weight >= 0


def test_animals_lifecycle():
    """
    Test the lifecycle of a herbivore; they start with age 0, which is
    incremented by one for every year passed. They eat and gains weight, and
    loose weight for every year.
    """
    herb = Herbivore()
    assert herb.age == 0
    herb.aging()
    start_weight = herb.weight
    herb.eating(100)
    assert herb.weight > start_weight
    assert herb.age == 1
    new_weight = herb.weight
    herb.weight_loss()
    assert herb.weight < new_weight




def test_animals_fitness():
    """Tests that the fitness of a Herbivore is between 0 and 1, and works
    as expected.
    """
    herb = Herbivore()
    value1 = herb.fitness
    assert 0 <= value1 <= 1
    herb.aging()
    value2 = herb.fitness
    assert value2 < value1
    herb.weight_loss()
    value3 = herb.fitness
    assert value3 < value2

    carn = Carnivore()
    value1 = carn.fitness
    assert 0 <= value1 <= 1
    carn.aging()
    value2 = carn.fitness
    assert value2 < value1
    carn.weight_loss()
    value3 = carn.fitness
    assert value3 < value2
    
    
def test_animals_reproduction_probability():
    """
    Tests that the Herbivore reproduce after given specifications.
    """
    herb = Herbivore(weight=30)
    assert not herb.reproduction_probability(n_animals=1)[0]
    herb2 = Herbivore(weight=50)
    assert not herb2.reproduction_probability(n_animals=1)[0]
    assert herb2.reproduction_probability(n_animals=1000)[0]
    herb3 = Herbivore(weight=2)
    assert not herb3.reproduction_probability(n_animals=1000)[0]

    carn = Carnivore(weight=30)
    assert not carn.reproduction_probability(n_animals=1)[0]
    carn2 = Carnivore(weight=50)
    assert not carn2.reproduction_probability(n_animals=1)[0]
    assert carn2.reproduction_probability(n_animals=1000)[0]
    carn3 = Carnivore(weight=2)
    assert not carn3.reproduction_probability(n_animals=1000)[0]


def test_animal_update_weight_after_birth():
    """
    Tests that a herbivore weight is reduced following birth.
    """
    newborn_weight = 8
    initial_weight = 50
    herb = Herbivore(weight=initial_weight)
    herb.update_weight_after_birth(newborn_weight=newborn_weight)
    assert herb.weight < initial_weight
    assert herb.weight == approx(initial_weight - (
            herb.default_parameters["xi"] * newborn_weight
    ), rel=1e-1)

    newborn_weight = 8
    initial_weight = 50
    carn = Carnivore(weight=initial_weight)
    carn.update_weight_after_birth(newborn_weight=newborn_weight)
    assert carn.weight < initial_weight
    assert carn.weight == approx(initial_weight - (
            carn.default_parameters["xi"] * newborn_weight
    ), rel=1e-1)


def test_animal_death():
    """
    Tests that animals die with certainty 1 if its fitness is 0, and dies
    with certainty 0 if its fitness is 1, according to the given formula for
    the probability of animal death.
    """
    herb = Herbivore()
    herb.default_parameters['omega'] = 1
    herb.phi = 0
    assert herb.death()
    herb.phi = 1
    assert not herb.death()

    carn = Carnivore()
    carn.default_parameters['omega'] = 1
    carn.phi = 0
    assert carn.death()
    carn.phi = 1
    assert not carn.death()


def test_herbivore_eating():
    """

    """
    herb = Herbivore()
    initial_weight = herb.weight
    herb.eating(fodder=10)
    new_weight = herb.weight
    assert new_weight > initial_weight


def test_carnivore_eating_probability():
    herb = Herbivore()
    herb.fitness = 0.7
    carn = Carnivore()
    carn.fitness = 0.3
    assert not carn.eating_probability()
    carn.fitness = 0.8


def test_carnivore_eating():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 15},
           {'species': 'Herbivore', 'age': 5, 'weight': 40},
           {'species': 'Herbivore', 'age': 15, 'weight': 25},
           {'species': 'Herbivore', 'age': 17, 'weight': 20},
           {'species': 'Herbivore', 'age': 8, 'weight': 30},
           {'species': 'Herbivore', 'age': 20, 'weight': 35}]



