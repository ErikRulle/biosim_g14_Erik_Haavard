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
    assert list(herb.default_parameters.keys()) in keys_list


def test_carnivore_parameters():
    """
    Tests that the given parameters for the carnivore class are in the list
     of valid parameters.
    """
    keys_list = ['w_birth', 'sigma_birth', 'beta', 'eta', 'a_half', 'phi_age',
                 'w_half', 'phi_weight', 'mu', 'lambda', 'gamma', 'zeta',
                 'xi', 'omega', 'F', 'DeltaPhiMax']
    carn = Carnivore()
    assert carn.default_parameters.keys() in keys_list


def test_non_negative_herbivore_weight():
    """Tests that animals has a non-negative weight."""
    herb = Herbivore()
    assert isinstance(herb, Herbivore)
    assert herb.weight >= 0


def test_herbivore_lifecycle():
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


def test_herbivore_fitness():
    """Tests that the fitness of a Herbivore is between 0 and 1, and works
    as expected.
    """
    herb = Herbivore()
    herb.calculate_fitness()
    value1 = herb.phi
    assert 0 <= value1 <= 1
    herb.aging()
    herb.calculate_fitness()
    value2 = herb.phi
    assert value2 < value1
    herb.weight_loss()
    herb.calculate_fitness()
    value3 = herb.phi
    assert value3 < value2
    
    
def test_herbivore_reproduction_probability():
    """
    Tests that the Herbivore reproduce after given specifications.
    """
    herb = Herbivore(weight=33)
    herb.calculate_fitness()
    assert not herb.reproduction_probability(n_animals=10)
    herb2 = Herbivore(weight=50)
    herb2.calculate_fitness()
    assert not herb2.reproduction_probability(n_animals=1)
    assert herb2.reproduction_probability(n_animals=1000)
    herb3 = Herbivore(weight=2)
    assert not herb3.reproduction_probability(n_animals=1000)


def test_herbivore_update_weight_after_birth():
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
    ))


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
