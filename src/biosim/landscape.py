# -*- coding: utf-8 -*-

"""
:mod:`biosim.landscape` defines how a landscape object should behave and how
its animal population interact with each other and their surroundings. The
subclasses, Jungle, Savannah, Desert, Mountain and Ocean, contains information
about the differences between each landscape type, e.g. availability and
regeneration of fodder.
"""

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


import numpy as np
import random

import biosim.animals as ba


class Landscape:
    """
    This class decides the behaviour of the landscape.
    """

    default_parameters = {"f_max": 0}
    habitable = None

    def __init__(self):
        """
        This method creates variables needed for the class.
        """
        self.f = self.default_parameters["f_max"]
        self.animal_population = [[], []]
        self.new_population = [[], []]

    @classmethod
    def set_landscape_parameters(cls, new_parameters):
        """
        This method allows for manual setting of landscape parameters,
        i.e. to change parameter values from default values to desired values.

        :param new_parameters: dict, dictionary with the new parameter values.
                               Only keys from the default parameter value dict
                               are valid.
        """
        for key in new_parameters:
            cls.default_parameters[key] = new_parameters[key]

    def cell_population(self, population=None):
        """
        Puts the animal population in the specific cell.

        :param population: list.
        """
        for animal in population:
            if animal["species"] == "Herbivore":
                self.animal_population[0].append(ba.Herbivore(
                    age=animal["age"], weight=animal["weight"]))
            else:
                self.animal_population[1].append(ba.Carnivore(
                    age=animal["age"], weight=animal["weight"]))

    @property
    def number_of_herbivores(self):
        """
        Finds the total number of herbivores in a specific cell.

        :return: integer, number of herbivores.
        """
        return len(self.animal_population[0])

    @property
    def number_of_carnivores(self):
        """
        Finds the total number of carnivores in a specific cell.

        :return: integer, number of carnivores.
        """
        return len(self.animal_population[1])

    @property
    def sum_of_herbivore_mass(self):
        """
        Calculates the total herbivore mass in the specific cell, i.e. the
        sum of the herbivore weights.

        :return: integer, the sum of herbivore mass in the cell.
        """
        return sum([herb.weight for herb in self.animal_population[0]])

    def sort_by_fitness(self):
        """
        Updates and sorts animals in a specific cell by fitness, in descending
        order.
        """
        self.animal_population[0] = sorted(self.animal_population[0],
                                           key=lambda x: x.fitness,
                                           reverse=True)
        self.animal_population[1] = sorted(self.animal_population[1],
                                           key=lambda x: x.fitness,
                                           reverse=True)

    def update_fitness(self):
        """
        Updates the fitness for all animals in the cell.
        """
        for species in self.animal_population:
            for animal in species:
                animal.fitness

    def weight_loss(self):
        """
        Reduces weight of all animals once a year.
        """
        for species in self.animal_population:
            for animal in species:
                animal.animal_weight_loss()
                
    def aging(self):
        """
        The age of all animals in the specific cell is incremented by one,
        once a year.
        """

        for species in self.animal_population:
            for animal in species:
                animal.aging()

    def death(self):
        """
        Updates the animal population list with the surviving animals after
        every year.
        """

        self.animal_population[0] = [
            animal for animal in self.animal_population[0] if not
            animal.death()
        ]
        self.animal_population[1] = [
            animal for animal in self.animal_population[1] if not
            animal.death()
        ]

    def reproduction(self):
        """
        Finds out which animals for each species that reproduce, based on
        reproduction probability, and adds a newborn of that species
        to the cell.
        """
        for species in self.animal_population:
            newborn_animals = []
            for animal in species:
                if animal.reproduction_probability(len(species)):
                    if isinstance(animal, ba.Herbivore):
                        newborn_animals.append(ba.Herbivore())
                    elif isinstance(animal, ba.Carnivore):
                        newborn_animals.append(ba.Carnivore())
                    animal.update_weight_after_birth()
            species.extend(newborn_animals)

    def eat_request_herbivore(self):
        """
        Herbivores eats after request and update of available fodder.
        """
        for herbivore in self.animal_population[0]:
            request = herbivore.default_parameters["F"]
            if request <= self.f:
                self.f -= request
            else:
                request = self.f
                self.f = 0
            herbivore.eating(request)

    def eat_request_carnivore(self):
        """
        Carnivore eats after request.
        """
        for carnivore in self.animal_population[1]:
            self.animal_population[0] = carnivore.eating(
                self.animal_population[0])

    @property
    def available_fodder_herbivore(self):
        """
        Finding the relative abundance of fodder for herbivore.

        :return: float.
        """
        return self.f / ((self.number_of_herbivores + 1) *
                         ba.Herbivore.default_parameters["F"])

    @property
    def available_fodder_carnivore(self):
        """
        Finding the relative abundance of fodder for carnivore.

        :return: float.
        """
        return self.sum_of_herbivore_mass / (
                (self.number_of_carnivores + 1) *
                ba.Carnivore.default_parameters["F"])

    def propensity(self):
        """
        Calculates the propensity of an animal migrating.

        :return: tuple, the propensities of herbivore and carnivore migration
                 in first and second element of the tuple, respectively.
        """
        herbivore_propensity = np.exp(
                    ba.Herbivore.default_parameters["lambda"] *
                    self.available_fodder_herbivore)

        carnivore_propensity = np.exp(
                    ba.Carnivore.default_parameters["lambda"] *
                    self.available_fodder_carnivore)

        if self.habitable:
            return tuple([herbivore_propensity, carnivore_propensity])
        else:
            return tuple([0, 0])

    def directional_probability(self, animal, neighbour_cells):
        """
        This method estimates the propensity for each neighbouring cell, and
        calculates the probability of herbivores migrating to that cell.
        Stores the result in a list.

        :param animal: object, either herbivore or carnivore.
        :param neighbour_cells: list, the four adjacent cells.
        :return probability_list: list, probabilities of moving to an
                                  adjacent cell.
        """
        if isinstance(animal, ba.Herbivore):
            propensities = [cell.propensity()[0]
                            for cell in neighbour_cells]
            probability_list = [propensity / sum(propensities)
                                for propensity in propensities]
        else:
            propensities = [cell.propensity()[1]
                            for cell in neighbour_cells]
            probability_list = [propensity / sum(propensities)
                                for propensity in propensities]
        return probability_list

    def choose_migration_cell(self, animal, neighbour_cells, probability_list):
        """
        A method to choose which of the adjacent cell the animal should
        migrate to, given that it migrates, and moves the animal to that cell.

        :param animal: object, either herbivore or carnivore.
        :param probability_list: list, probabilities of moving to an adjacent
                                 cell.
        :param neighbour_cells: list, objects of adjacent cells.
        """
        p = random.random()
        i = 0
        while p > sum(probability_list[0:i]):
            i += 1
        animal.move(neighbour_cells[i - 1])

    def migrate(self, neighbour_cells):
        """
        A method that migrates all animals in a cell iteratively.

        :param neighbour_cells: list, objects of adjacent cells.
        """
        for species in self.animal_population:
            if len(species) > 0:
                probability_list = self.directional_probability(
                    species[0], neighbour_cells)
                for animal in species:
                    if animal.migration_probability():
                        self.choose_migration_cell(
                            animal, neighbour_cells, probability_list)
                    else:
                        if isinstance(animal, ba.Herbivore):
                            ba.Herbivore.move(animal, cell=self)
                        elif isinstance(animal, ba.Carnivore):
                            ba.Carnivore.move(animal, cell=self)

    def update_cell_population(self):
        """
        Updates the animal population in the specific cell.
        """
        self.animal_population = self.new_population
        self.new_population = [[], []]


class Jungle(Landscape):
    """
    Defines the jungle type.
    """
    default_parameters = {"f_max": 800.0}
    habitable = True

    def regenerate(self):
        """
        This method regenerates the amount of fodder in each jungle-cell
        according to the equation

        .. math::

            f_{ij} \gets f_{max}^{Jungle}

        """
        self.f = self.default_parameters["f_max"]


class Savannah(Landscape):
    """
    Defines the savannah type.
    """
    default_parameters = {"f_max": 300.0, "alpha": 0.3}
    habitable = True

    def regenerate(self):
        """
        This method regenerates the amount of fodder in each savannah-cell
        according to the equation

        .. math::

            f_{ij} \gets f_{ij} + \\alpha \\times (f_{max}^{Sav} - f_{ij}),

        where :math:`\alpha` is a parameter value for the svannah landscape
        type
        """
        self.f += self.default_parameters["alpha"] * \
                  (self.default_parameters["f_max"] - self.f)


class Desert(Landscape):
    """
    Defines the desert type.
    """
    default_parameters = {"f_max": 0.0}
    habitable = True


class Mountain(Landscape):
    """
    Defines the mountain type.
    """
    default_parameters = {"f_max": 0.0}
    habitable = False


class Ocean(Landscape):
    """
    Defines the ocean type.
    """
    default_parameters = {"f_max": 0.0}
    habitable = False
