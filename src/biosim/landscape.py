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

    @property
    def sum_of_herbivore_mass(self):
        """
        Calculates the total herbivore mass in the specific cell, i.e. the
        sum of the herbivore weights.

        :return: integer, the sum of herbivore mass in the cell
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
                    if isinstance(animal, Herbivore):
                        newborn_animals.append(Herbivore())
                    elif isinstance(animal, Carnivore):
                        newborn_animals.append(Carnivore())
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

    def regenerate(self):
        """
        This method regenerates the amount of fodder in each cell according to
        given formula for the given landscape type.
        """
        if self.f != self.default_parameters["f_max"]:
            if isinstance(self, Jungle):
                self.f = self.default_parameters["f_max"]
            elif isinstance(self, Savannah):
                self.f += self.default_parameters["alpha"] * \
                          (self.default_parameters["f_max"] - self.f)


class Jungle(Landscape):
    """
    Defines the jungle type
    """
    default_params = {'f_max': 800.0}


class Savannah(Landscape):
    """
    Defines the savannah type
    """
    default_params = {'f_max': 300.0, 'alpha': 0.3}


class Desert(Landscape):
    """
    Defines the desert type
    """
    default_params = {'f_max': 0.0}


class Mountain(Landscape):
    """
    Defines the mountain type
    """
    default_params = {'f_max': 0.0}


class Ocean(Landscape):
    """
    Defines the ocean type
    """
    default_params = {'f_max': 0.0}


