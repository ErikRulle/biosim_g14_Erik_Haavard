# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


from biosim.animals import *


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

    def set_landscape_parameters(self, new_parameters):
        """
        This method allows for manual setting of landscape parameters,
        i.e. to change parameter values from default values to desired values.

        :param new_parameters: dict, dictionary with the new parameter values
                               Only keys from the default parameter value dict
                               are valid.
        """
        for key in new_parameters:
            self.default_parameters[key] = new_parameters[key]

    def cell_population(self, population=None):
        """
        Puts the animal population in the specific cell.
        :param population: list
        """
        for animal in population:
            if animal["species"] == "Herbivore":
                self.animal_population[0].append(Herbivore(
                    age=animal["age"], weight=animal["weight"]))
            else:
                self.animal_population[1].append(Carnivore(
                    age=animal["age"], weight=animal["weight"]))

    @property
    def number_of_herbivores(self):
        """
        Finds the total number of herbivores in a specific cell

        :return: integer, number of herbivores.
        """
        return len(self.animal_population[0])

    @property
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
        """
        self.animal_population[0] = sorted(self.animal_population[0],
                                           key=lambda x: x.fitness,
                                           reverse=True)
        self.animal_population[1] = sorted(self.animal_population[1],
                                           key=lambda x: x.fitness,
                                           reverse=True)

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

