# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad, Håvard Molversmyr"
__email__ = "erikrull@nmbu.no, havardmo@nmbu.no"

"""
:mod:`biosim.animals` defines ... and returns ...

The user can define:
#.
#.

If different sizes of the population within an species is preferable,
the user can simply make another population and add it to the island

Example of ... returned:
-------------------------
::

"""

import numpy as np
import random


class Animals:
    """
    This class creates an idea Animal, not specifying the vore-type.
    """

    default_parameters = {"w_birth": None, "sigma_birth": None, "beta": None,
                          "eta": None, "a_half": None, "phi_age": None,
                          "w_half": None, "phi_weight": None, "mu": None,
                          "lambda": None, "gamma": None, "zeta": None,
                          "xi": None, "omega": None, "F": None,
                          "DeltaPhiMax": None}

    def __init__(self, weight=default_parameters["w_birth"], age=0):
        """
        This method creates variables needed for the class.

        :param weight: float, weight of the animals
        :param age: int, age of the animal
        """

        if age == 0:
            self.weight = random.normalvariate(
                weight, self.default_parameters["sigma_birth"]
            )
        else:
            self.weight = weight
        self.age = age
        #self._phi = self.fitness
        #self._phi = None

    def set_animal_parameters(self, new_parameters):
        """
        This method allows for manual setting of animal parameters,
        i.e. to change parameter values from default values to desired values.

        :param new_parameters: dict, dictionary with the new parameter values
                               Only keys from the default parameter value dict
                               are valid.
        """
        for key in new_parameters:
            self.default_parameters[key] = new_parameters[key]

    def aging(self):
        """
        Animal ages by one year.
        """
        self.age += 1

    def check_weight(self):
        """
        Checks the weight of the animal.
        """
        return self.weight

    def animal_weight_loss(self):
        """
        Updates animal weight after annual weight loss.
        """
        self.weight -= self.default_parameters["eta"] * self.weight

    def reproduction_probability(self, n_animals):
        """
        Estimates the probability of reproduction for the given animal.

        :param n_animals: integer, number of animals that may reproduce
        :return reproduction_success: bool, the animal reproduces or not.
                newborn_weight: float, weight of the newborn animal.
        """
        newborn_weight = random.normalvariate(
            self.default_parameters["w_birth"],
            self.default_parameters["sigma_birth"]
        )

        if self.weight < self.default_parameters["zeta"] * (
                self.default_parameters["w_birth"] + (
                self.default_parameters["sigma_birth"])):
            reproduction_prob = 0
        elif self.weight < newborn_weight:
            reproduction_prob = 0
        else:
            reproduction_prob = min(
                [1, self.default_parameters["gamma"] * self.fitness * (
                        n_animals - 1)])

        reproduction_success = random.random() <= reproduction_prob
        return reproduction_success, newborn_weight

    def update_weight_after_birth(self, newborn_weight):
        """
        If reproduction is successful, then a new animal is born, and the
        mother"s weight is reduced by the baby"s birthweight.

        :param newborn_weight: float, weight of newborn animal
        """
        self.weight -= self.default_parameters["xi"] * newborn_weight

    def death(self):
        """
        Estimates the probability of an animal dying.

        :return: bool
        """
        death_prob = self.default_parameters["omega"] * (1 - self.fitness)
        return random.random() < death_prob

    @property
    def fitness(self):
        """
        Calculates the fitness of the animal.

        :return: float
        """

        self._phi = 1 / (1 + np.exp(self.default_parameters["phi_age"] * (
                    self.age - self.default_parameters["a_half"]
            ))) * 1 / (1 + np.exp(
                -self.default_parameters["phi_weight"] * (
                        self.weight - self.default_parameters["w_half"])))

        return self._phi

    @fitness.setter
    def fitness(self, value):
        """
        A setter for the property attribute fitness, to allow for testing of
        the code.
        """
        self._phi = value


    def migrate(self):
        pass


class Herbivore(Animals):
    """
    A subclass of the superclass Animals, which creates a herbivore with its
    default parameters.
    """

    default_parameters = {"w_birth": 8.0, "sigma_birth": 1.5, "beta": 0.9,
                          "eta": 0.05, "a_half": 40.0, "phi_age": 0.2,
                          "w_half": 10.0, "phi_weight": 0.1, "mu": 0.25,
                          "lambda": 1.0, "gamma": 0.2, "zeta": 3.5,
                          "xi": 1.2, "omega": 0.4, "F": 10.0}

    def __init__(self, weight=None, age=0):
        """
        Creates the variables needed for the subclass.
        """
        if weight is None:
            weight = self.default_parameters["w_birth"]
        super().__init__(weight=weight, age=age)

    def eating(self, fodder):
        """
        Caculates the new weight of the herbivore after eating fodder.

        :param fodder: float, amount of fodder eaten by the herbivore.
        """
        self.weight += fodder * self.default_parameters["beta"]


class Carnivore(Animals):
    """
    A subclass of the superclass Animals, which creates a carnivore with its
    default parameters.
    """

    default_parameters = {"w_birth": 6.0, "sigma_birth": 1.0, "beta": 0.75,
                          "eta": 0.125, "a_half": 60.0, "phi_age": 0.4,
                          "w_half": 4.0, "phi_weight": 0.4, "mu": 0.4,
                          "lambda": 1.0, "gamma": 0.8, "zeta": 3.5,
                          "xi": 1.1, "omega": 0.9, "F": 50.0, 
                          "DeltaPhiMax": 10.0}

    def __init__(self, weight=None, age=0):
        """
        Creates the variables needed for the subclass.
        """
        if weight is None:
            weight = self.default_parameters["w_birth"]
        super().__init__(weight=weight, age=age)

    def eating_probability(self, herbivores):
        """

        :param herbivores: list of herbivores
        :return:
        """
        delta_phi_max = self.default_parameters["DeltaPhiMax"]

        if self.fitness <= herbivores.fitness:
            return 0
        elif 0 < self.fitness - herbivores.fitness < deltafitness_max:
            return (self.fitness - herbivores.fitness) / deltafitness_max
        else:
            return 1

    def eating(self, herbivores):
        """
        Calculates the new weight of the carnivore after eating fodder.
        :param herbivores: float, amount of fodder eaten by the herbivore.
        """
        weight_eaten = 0
        max_feed = self.default_parameters["F"]

        for herbivore in herbivores[::-1]:
            if weight_eaten < max_feed \
                    and random.random() < self.eating_probability(herbivore):
                if weight_eaten + herbivore.weight > max_feed:
                    herbivore.weight = max_feed - weight_eaten
                    self.weight += (
                            self.default_parameters["beta"] * herbivore.weight
                    )
                    weight_eaten = max_feed

                else:
                    self.weight += (
                            self.default_parameters["beta"] * herbivore.weight
                    )
                    weight_eaten += herbivore.weight
