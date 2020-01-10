# -*- coding: utf-8 -*-

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


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
        self.pop_animals = [[], []]


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

