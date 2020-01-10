# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


from src.biosim.animals import *


class Landscape:
    """
    This class decides the behaviour of the landscape.
    """

    default_parameters = {'f_max': 0}

    def __init__(self):
        """
        This method creates variables needed for the class.
        """
        self.f = self.default_parameters['f_max']
        self.animal_population = [[], []]

    def cell_population(self, population=None):
        """
        Puts the animal population in the specific cell.
        :param population: list
        :return:
        """
        for animal in population:
            if animal["species"] == "Herbivore":
                self.animal_population[0].append(Herbivore(
                    age=animal["age"], weight=animal["weight"]))
            else:
                self.animal_population[1].append(Carnivore(
                    age=animal["age"], weight=animal["weight"]))

    def number_of_herbivores(self):
        """
        Finds the total number of herbivores in a specific cell
        :return: integer, number of herbivores.
        """
        return len(self.animal_population[0])

    def number_of_carnivores(self):
        """
        Finds the total number of carnivores in a specific cell
        :return: integer, number of carnivores.
        """
        return len(self.animal_population[1])

    def sort_by_fitness(self):
        """
        Updates and sorts animals in a specific cell by fitness, in descending
        order.
        :return:
        """
        for species in self.animal_population:
            for animal in species:
                animal.calculate_fitness()

        for species in self.animal_population:
            for index in range(len(species)):
                for animal in range(len(species) - index - 1):
                    if species[animal].phi < species[animal + 1].phi:
                        species[animal], species[animal + 1] = \
                            species[animal + 1], species[animal]

    def weight_loss(self):
        """
        Reduces weight of all animals once a year.
        :return:
        """
        for species in self.animal_population:
            for animal in species:
                animal.weight_loss()


    def available_fodder_herbivore(self):
        """
        Calculates the available fodder for herbivores in the landscape
        :return fodder_amount:
        """
        pass

    def counter(self):
        """
        This method counts the number of herbivores and carnivores in each
        cell.

        :return:
        """
        pass

    def weight_loss(self):
        """
        This method estimates the new weight after loss of weight

        :return: New weight of animals
        """
        pass


class Jungle(Landscape):
    """
    Defines the jungle type
    """

    def __init__(self):
        pass

    def regenerate(self):
        """
        This method regenerates the amount of fodder in each cell according to
        given formula for the jungle type.
        """
        pass



class Savannah(Landscape):
    """
    Defines the savannah type
    """

    def __init__(self):
        """
        This method creates variables needed for the class.
        """
        pass

    def regenerate(self):
        """
        This method regenerates the amount of fodder in each cell according to
        given formula for the savannah type.
        """
        pass


class Desert(Landscape):
    """
    Defines the desert type
    """

    def __init__(self):
        """
        This method creates variables needed for the class.
        """
        pass


class Mountain(Landscape):
    """
    Defines the mountain type
    """

    def __init__(self):
        """
        This method creates variables needed for the class.
        """
        pass


class Ocean(Landscape):
    """
    Defines the ocean type
    """

    def __init__(self):
        """
        This method creates variables needed for the class.
        """
        pass

