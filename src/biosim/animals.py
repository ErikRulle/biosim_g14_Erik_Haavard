# -*- coding: utf-8 -*-

"""
:mod:`biosim.animals` defines the similar traits between our two animals in
the ecosystem. The two subclasses, Herbivore and Carnivore, specifies the
more specific traits that are intrinsic for each animal. The module returns
either herbivore or carnivore objects, depending on what the simulation is
calling for.

The user can define:
    * The user can define the species of the animal.
    * The weight and age can be specified.
"""

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


import math
import random


class Animal:
    """
    This class creates an idea Animal, not specifying the -vore-type.
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

        :param weight: float, weight of the animal.
        :param age: int, age of the animal.
        """

        self._phi = None    # Initialised by fitness property
        self._recompute_phi = True

        if age == 0:
            self.weight = random.normalvariate(
                weight, self.default_parameters["sigma_birth"]
            )
        else:
            self.weight = weight
        self.age = age
        self.newborn_weight = random.normalvariate(
            self.default_parameters["w_birth"],
            self.default_parameters["sigma_birth"]
        )

    @classmethod
    def set_animal_parameters(cls, new_parameters):
        """
        This method allows for manual setting of animal parameters,
        i.e. to change parameter values from default values to desired values.

        The parameters :math:`w_{birth},\\sigma_{birth}, \\beta, \\eta,
        a_\\frac{1}{2}, \\phi_{age}, w_\\frac{1}{2}, \\phi_{weight}, \\mu,
        \\lambda, \\gamma, \\zeta, \\xi, \\omega, F` and
        :math:`\\Delta\\Phi_{max}` are identical for all animals of the same
        species, but may be different between herbivores and carnivores.

        :param new_parameters: dict, dictionary with the new parameter values.
                               Only keys from the default parameter value dict
                               are valid.
        """
        for key in new_parameters:
            cls.default_parameters[key] = new_parameters[key]

    def aging(self):
        """
        Animal ages by one year.
        """
        self.age = self.age + 1

    @property
    def age(self):
        """
        Returns the animals age
        """
        return self._age

    @age.setter
    def age(self, new_age):
        """
        Sets the age of the animals to the new value, and flags the fitness
        attribute so that it will be recomputed the next time it is called.
        """
        self._age = new_age
        self._recompute_phi = True

    @property
    def weight(self):
        """
        Returns the animals weight.
        """
        return self._weight

    @weight.setter
    def weight(self, new_weight):
        """
        Sets the weight of the animals to the new value, and flags the fitness
        attribute so that it will be recomputed the next time it is called.
        """
        self._weight = new_weight
        self._recompute_phi = True

    def animal_weight_loss(self):
        """
        Updates animal weight after annual weight loss with  a decrease rate
        of :math:`\\eta w`, where :math:`\\eta` is a parameter value for the
        animal, and :math:`w` is the animal's current weight.
        """
        self.weight = self.weight - (
                self.default_parameters["eta"] * self.weight
        )

    def reproduction_probability(self, n_animals):
        """
        Estimates the probability of reproduction for the given animal
        according to the equation

        .. math::

            min(1, \gamma \\times \phi \\times (N-1),

        where :math:`N` is the number of conspecific animals at the start of
        the breeding season, and :math:`\\gamma` and :math:`\\phi` are
        species-specific parameter values. This means that the reproduction
        probability is 0 if there is only one individual of a species in the
        given cell.

        Furthermore, the probability is also 0 if the weight is

        .. math::

            w < \\zeta (w_{birth} + \sigma_{birth}),

        where :math:`\\zeta, w_{birth}` and :math:`\\sigma_{birth}` are all
        species-specific parameter values.

        :param n_animals: integer, number of animals that may reproduce.
        :return reproduction_success: bool, the animal reproduces or not.
        """

        if self.weight < self.default_parameters["zeta"] * (
                self.default_parameters["w_birth"] + (
                self.default_parameters["sigma_birth"])):
            reproduction_prob = 0
        elif self.weight < self.newborn_weight:
            reproduction_prob = 0
        else:
            reproduction_prob = min(
                [1, self.default_parameters["gamma"] * self.fitness * (
                        n_animals - 1)])

        reproduction_success = random.random() <= reproduction_prob
        return reproduction_success

    def update_weight_after_birth(self):
        r"""
        If reproduction is successful  a new animal is born, and the mother's
        weight is reduced by the equation

        .. math::

            w = \xi * N(w_{birth}, \sigma_{birth}),

        where :math:`N(w_{birth}, \sigma_{birth})` is the newborn's weight
        that is normally distributed with mean :math:`w_{birth}` and
        standard deviation :math:`\sigma_{birth}`, and :math:`\xi` is a
        parameter value for the animal.
        """
        self.weight = self.weight - (
                self.default_parameters["xi"] * self.newborn_weight
        )

    def death(self):
        """
        Estimates the probability of an animal dying, given by the equation

        .. math::

            \\omega(1-\\phi)

        :return: bool.
        """
        death_prob = self.default_parameters["omega"] * (1 - self.fitness)
        return random.random() < death_prob

    @property
    def fitness(self):
        """
        Calculates the fitness of the animal, given by the equation

        .. math::

            \Phi
            =
            \Biggl \lbrace
            {
            0, {w ≤ 0}
            \\atop
            q^{+}(a, a_{\\frac{1}{2}}, \phi_{age}) \\times q^{-}(w, w_{\\frac
            {1}{2}}, \phi_{weight}), \\text{ else }
            }

        where

        .. math::

            q^{\pm}(x, x_{\\frac{1}{2}}, \phi) = \\frac{1}{1 + e^{\pm \phi(x
             - x_{\\frac{1}{2}})}}

        :return: float.
        """

        if not self._recompute_phi:
            return self._phi
        else:
            self._phi = 1 / (1 + math.exp(self.default_parameters["phi_age"] *
                                          (
                        self.age - self.default_parameters["a_half"]
                ))) * 1 / (1 + math.exp(
                    -self.default_parameters["phi_weight"] * (
                            self.weight - self.default_parameters["w_half"])))
            self._recompute_phi = False

            return self._phi

    def migration_probability(self):
        """
        Probability for the animal to migrate. The probability is calculated
        as :math:`\mu \Phi`.

        :return: bool.
        """
        migration_probability = random.random() <= (
                self.default_parameters["mu"] * self.fitness
        )
        return migration_probability


class Herbivore(Animal):
    """
    A subclass of the superclass Animal, which creates a herbivore with its
    default parameters.
    """

    default_parameters = {"w_birth": 8.0, "sigma_birth": 1.5, "beta": 0.9,
                          "eta": 0.05, "a_half": 40.0, "phi_age": 0.2,
                          "w_half": 10.0, "phi_weight": 0.1, "mu": 0.25,
                          "lambda": 1.0, "gamma": 0.2, "zeta": 3.5,
                          "xi": 1.2, "omega": 0.4, "F": 10.0}

    def __init__(self, weight=None, age=0):
        """
        Creates the variables needed for the subclass. Inherits the
        constructor of superclass.
        """
        if weight is None:
            weight = self.default_parameters["w_birth"]
        super().__init__(weight=weight, age=age)

    def eating(self, fodder):
        """
        Calculates the new weight of the herbivore after eating fodder.
        Given that a herbivore eats an amount :math:`\\tilde{F}` of fodder,
        it's weight increases by :math:`\\beta \\tilde{F}`, where
        :math:`\\beta` is a parameter value specific for herbivores.


        :param fodder: float, amount of fodder eaten by the herbivore.
        """
        self.weight += fodder * self.default_parameters["beta"]

    def move(self, cell):
        """
        This method appends the herbivore to a list of the new population
        of the cell.

        :param cell: object, landscape type of the position in island map.
        """
        cell.new_population[0].append(self)


class Carnivore(Animal):
    """
    A subclass of the superclass Animal, which creates a carnivore with its
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
        Creates the variables needed for the subclass. Inherits the
        constructor of superclass.
        """
        if weight is None:
            weight = self.default_parameters["w_birth"]
        super().__init__(weight=weight, age=age)

    def eating_probability(self, herbivores):
        """
        Estimates the probability of a carnivore to eat a herbivore.
        Carnivores kill herbivores with probability

        .. math::

            p = \Biggl \lbrace
            {
            0, \\text{ if } {\Phi_{carn} ≤ \Phi_{herb}}
            \\atop
            \\frac{\Phi_{carn} - \Phi_{herb}}{\Delta\Phi_{max}}, \\text{ if }
            {0 < \Phi_{carn} - \Phi_{herb} < \Delta\Phi_{max}}
            }

        If neither of these conditions occur, the probability is 1.

        :param herbivores: list of herbivores.
        :return: float, probability of eating.
        """
        delta_phi_max = self.default_parameters["DeltaPhiMax"]

        if self.fitness <= herbivores.fitness:
            return 0
        elif 0 < self.fitness - herbivores.fitness < delta_phi_max:
            return (self.fitness - herbivores.fitness) / delta_phi_max
        else:
            return 1

    def eating(self, herbivores):
        """
        Calculates the new weight of the carnivore after eating fodder.
        The carnivores weight increases by :math:`\\beta w_{herb}`, where
        :math:`w_{herb}` is the weight of the herbivore killed, or the
        weight amount of the herbivore that the carnivore eats to
        become satiated.

        :param herbivores: float, amount of fodder eaten by the herbivore.
        :return herbivores_not_eaten: list of surviving herbivores.
        """
        herbivores_not_eaten = []
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
            else:
                herbivores_not_eaten.append(herbivore)

        return herbivores_not_eaten

    def move(self, cell):
        """
        This method appends the carnivore to a list of the new population
        of the cell.

        :param cell: object, landscape type of the position in map.
        """
        cell.new_population[1].append(self)
