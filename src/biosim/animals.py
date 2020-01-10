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

    default_parameters = {'w_birth': None, 'sigma_birth': None, 'beta': None,
                          'eta': None, 'a_half': None, 'phi_age': None,
                          'w_half': None, 'phi_weight': None, 'mu': None,
                          'lambda': None, 'gamma': None, 'zeta': None,
                          'xi': None, 'omega': None, 'F': None,
                          'DeltaPhiMax': None}

    def __init__(self, weight=default_parameters['w_birth'], age=0):
        """
        This method creates variables needed for the class.

        :param weight: float, weight of the animals
        :param age: int, age of the animal
        """

        self.weight = random.normalvariate(
            weight, self.default_parameters['sigma_birth']
        )
        self.age = age
        self.phi = 1 / (1 + np.exp(self.default_parameters['phi_age'] * (
                self.age - self.default_parameters['a_half']
        ))) * 1 / (1 + np.exp(-self.default_parameters['phi_weight'] * (
                    self.weight - self.default_parameters['w_half'])))

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

    def weight_loss(self):
        """
        Updates animal weight after annual weight loss.
        """
        self.weight -= self.default_parameters['eta'] * self.weight

    def reproduction(self, n_animals):
        """
        Estimates the probability of reproduction for the given animal.

        :param n_animals: integer, number of animals that can potentially
                                   reproduce.
        :return reproduction_success: bool, the animal reproduces or not.
        """
        if self.weight < self.default_parameters['zeta'] * (
                self.default_parameters['w_birth'] + (
                self.default_parameters['sigma_birth'])):
            reproduction_prob = 0
        else:
            reproduction_prob = min(
                [1, self.default_parameters['gamma'] * self.phi * (
                        n_animals - 1)])

        reproduction_success = random.random() <= reproduction_prob
        return reproduction_success

    def death(self):
        """
        Estimates the probability of an animal dying.

        :return: bool
        """
        death_prob = self.default_parameters['omega'] * (1 - self.phi)
        return random.random() < death_prob

    def calculate_fitness(self):
        """
        Calculates the fitness of the animal.

        :return: float
        """

        self.phi = 1 / (1 + np.exp(self.default_parameters['phi_age'] * (
                    self.age - self.default_parameters['a_half']
            ))) * 1 / (1 + np.exp(
                -self.default_parameters['phi_weight'] * (
                        self.weight - self.default_parameters['w_half'])))

        return self.phi

    def migrate(self):
        pass


class Herbivore(Animals):
    """
    A subclass of the superclass Animals, which creates a herbivore with its
    default parameters.
    """

    default_parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                          'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.2,
                          'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                          'lambda': 1.0, 'gamma': 0.2, 'zeta': 3.5,
                          'xi': 1.2, 'omega': 0.4, 'F': 10.0}

    def __init__(self, weight=None, age=0):
        """
        Creates the variables needed for the subclass.
        """
        if weight is None:
            weight = self.default_parameters['w_birth']
        super().__init__(weight=weight, age=age)

    def eating(self, fodder):
        """
        Caculates the new weight of the herbivore after eating fodder.

        :param fodder: float, amount of fodder eaten by the herbivore.
        """
        self.weight += fodder * self.default_parameters['beta']


class Carnivore(Animals):
    """

    """

    def __init__(self):
        pass
