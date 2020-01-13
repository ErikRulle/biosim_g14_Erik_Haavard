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


import biosim.animals as ba
import pytest


def test_set_animal_parameters():
    """
    Test that manual setting of animal parameters follows the given
    restrictions.
    """
    herb = ba.Herbivore()
    new_parameters = {"w_birth": 10, "sigma_birth": 1.5, "beta": 0.78,
                      "eta": 0.14, "a_half": 65.0, "phi_age": 0.5,
                      "w_half": 4.5, "phi_weight": 0.3, "mu": 0.5,
                      "lambda": 1.0, "gamma": 0.7, "zeta": 3.5,
                      "xi": 1.1, "omega": 0.9, "F": 30.0}
    herb.set_animal_parameters(new_parameters=new_parameters)
    assert new_parameters["eta"] <= 1
    for key in new_parameters.keys():
        assert new_parameters[key] >= 0

    carn = ba.Carnivore()
    new_parameters = {"w_birth": 10, "sigma_birth": 1.5, "beta": 0.78,
                      "eta": 0.14, "a_half": 65.0, "phi_age": 0.5,
                      "w_half": 4.5, "phi_weight": 0.3, "mu": 0.5,
                      "lambda": 1.0, "gamma": 0.7, "zeta": 3.5,
                      "xi": 1.1, "omega": 0.9, "F": 30.0,
                      "DeltaPhiMax": 10.0}
    carn.set_animal_parameters(new_parameters=new_parameters)
    assert new_parameters["DeltaPhiMax"] > 0
    assert new_parameters["eta"] <= 1
    for key in new_parameters.keys():
        if key is not "DeltaPhiMax":
            assert new_parameters[key] >= 0


def test_herbivore_parameters():
    """
    Tests that the given parameters for the herbivore class are in the list
     of valid parameters.
    """
    keys_list = ["w_birth", "sigma_birth", "beta","eta", "a_half", "phi_age",
                 "w_half", "phi_weight", "mu", "lambda", "gamma",  "zeta",
                 "xi", "omega", "F"]
    herb = ba.Herbivore()
    for key in keys_list:
        assert key in herb.default_parameters.keys()


def test_carnivore_parameters():
    """
    Tests that the given parameters for the carnivore class are in the list
     of valid parameters.
    """
    keys_list = ["w_birth", "sigma_birth", "beta", "eta", "a_half", "phi_age",
                 "w_half", "phi_weight", "mu", "lambda", "gamma", "zeta",
                 "xi", "omega", "F", "DeltaPhiMax"]
    carn = ba.Carnivore()
    for key in keys_list:
        assert key in carn.default_parameters.keys()


def test_non_negative_animal_weight():
    """Tests that animals has a non-negative weight."""
    herb = ba.Herbivore()
    carn = ba.Carnivore()
    assert isinstance(herb, ba.Herbivore)
    assert herb.weight >= 0
    assert isinstance(carn, ba.Carnivore)
    assert carn.weight >= 0


def test_animals_lifecycle():
    """
    Test the lifecycle of a herbivore; they start with age 0, which is
    incremented by one for every year passed. They eat and gains weight, and
    loose weight for every year.
    """
    herb = ba.Herbivore()
    assert herb.age == 0
    herb.aging()
    start_weight = herb.weight
    herb.eating(100)
    assert herb.weight > start_weight
    assert herb.age == 1
    new_weight = herb.weight
    herb.animal_weight_loss()
    assert herb.weight < new_weight


def test_animals_fitness():
    """Tests that the fitness of a Herbivore is between 0 and 1, and works
    as expected.
    """
    herb = ba.Herbivore()
    value1 = herb.fitness
    assert 0 <= value1 <= 1
    herb.aging()
    value2 = herb.fitness
    assert value2 < value1
    herb.animal_weight_loss()
    value3 = herb.fitness
    assert value3 < value2

    carn = ba.Carnivore()
    value1 = carn.fitness
    assert 0 <= value1 <= 1
    carn.aging()
    value2 = carn.fitness
    assert value2 < value1
    carn.animal_weight_loss()
    value3 = carn.fitness
    assert value3 < value2
    
    
def test_animals_reproduction_probability():
    """
    Tests that the Herbivore reproduce after given specifications.
    """
    herb = ba.Herbivore(weight=30)
    assert not herb.reproduction_probability(n_animals=1)
    herb2 = ba.Herbivore(weight=50)
    assert not herb2.reproduction_probability(n_animals=1)
    assert herb2.reproduction_probability(n_animals=1000)
    herb3 = ba.Herbivore(weight=2)
    assert not herb3.reproduction_probability(n_animals=1000)

    carn = ba.Carnivore(weight=30)
    assert not carn.reproduction_probability(n_animals=1)
    carn2 = ba.Carnivore(weight=50)
    assert not carn2.reproduction_probability(n_animals=1)
    assert carn2.reproduction_probability(n_animals=1000)
    carn3 = ba.Carnivore(weight=2)
    assert not carn3.reproduction_probability(n_animals=1000)


def test_animal_update_weight_after_birth():
    """
    Tests that a herbivore weight is reduced following birth.
    """
    newborn_weight = 8
    initial_weight = 50
    herb = ba.Herbivore(weight=initial_weight)
    herb.newborn_weight = 8
    herb.update_weight_after_birth()
    assert herb.weight < initial_weight
    assert herb.weight == pytest.approx(initial_weight - (
            herb.default_parameters["xi"] * newborn_weight
    ), rel=1e-1)

    newborn_weight = 8
    initial_weight = 50
    carn = ba.Carnivore(weight=initial_weight)
    carn.newborn_weight = 8
    carn.update_weight_after_birth()
    assert carn.weight < initial_weight
    assert carn.weight == pytest.approx(initial_weight - (
            carn.default_parameters["xi"] * newborn_weight
    ), rel=1e-1)


def test_animal_death(mocker):
    """
    Tests that animals die with certainty 1 if its fitness is 0, and dies
    with certainty 0 if its fitness is 1, according to the given formula for
    the probability of animal death.
    """
    herb = ba.Herbivore()
    herb.default_parameters["omega"] = 1
    mocker.patch("biosim.animals.Animals.fitness",
                 new_callable=mocker.PropertyMock, return_value=0)
    assert herb.death()
    mocker.patch("biosim.animals.Animals.fitness",
                 new_callable=mocker.PropertyMock, return_value=1)
    assert not herb.death()

    carn = ba.Carnivore()
    carn.default_parameters["omega"] = 1
    mocker.patch("biosim.animals.Animals.fitness",
                 new_callable=mocker.PropertyMock, return_value=0)
    assert carn.death()
    mocker.patch("biosim.animals.Animals.fitness",
                 new_callable=mocker.PropertyMock, return_value=1)
    assert not carn.death()


def test_herbivore_eating():
    """

    """
    herb = ba.Herbivore()
    initial_weight = herb.weight
    herb.eating(fodder=10)
    new_weight = herb.weight
    assert new_weight > initial_weight


def test_carnivore_eating_probability(mocker):
    herb = ba.Herbivore()
    mocker.patch("biosim.animals.Herbivore.fitness",
                 new_callable=mocker.PropertyMock, return_value=0.7)
    carn = ba.Carnivore()
    mocker.patch("biosim.animals.Carnivore.fitness",
                 new_callable=mocker.PropertyMock, return_value=0.3)
    assert not carn.eating_probability(herb)

    mocker.patch("biosim.animals.Herbivore.fitness",
                 new_callable=mocker.PropertyMock, return_value=0.2)
    mocker.patch("biosim.animals.Carnivore.fitness",
                 new_callable=mocker.PropertyMock, return_value=0.7)
    assert carn.eating_probability(herb) == pytest.approx(
        0.05
    )

    carn.set_animal_parameters({"DeltaPhiMax": 0.000001})
    assert carn.eating_probability(herb) == 1


@pytest.fixture(autouse=True)
def reset_parameters():
    ba.Carnivore.set_animal_parameters({"w_birth": 6.0, "sigma_birth": 1.0,
                                        "beta": 0.75, "eta": 0.125,
                                        "a_half": 60.0, "phi_age": 0.4,
                                        "w_half": 4.0, "phi_weight": 0.4,
                                        "mu": 0.4, "lambda": 1.0, "gamma": 0.8,
                                        "zeta": 3.5, "xi": 1.1, "omega": 0.9,
                                        "F": 50.0, "DeltaPhiMax": 10.0})


def test_carnivore_eating():
    herbivores = [ba.Herbivore(weight=15, age=5) for _ in range(6)]
    ba.Carnivore.set_animal_parameters({"DeltaPhiMax": 0.000001})
    carn = ba.Carnivore(weight=500, age=5)
    start_weight = carn.weight
    surviving_herbivores = carn.eating(herbivores)
    new_weight = carn.weight
    assert len(herbivores) > len(surviving_herbivores)
    assert new_weight > start_weight
    assert carn.weight == 537.5



