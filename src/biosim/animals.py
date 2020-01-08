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


class Animals:
    def __init__(self):
        """
        This method creates variables needed for the class.
        """
        pass

    def weight(self):
        pass

    def weight_loss(self):
        pass

    def age(self):
        pass

    def eat(self):
        pass

    def mate(self):
        pass

    def calculate_fitness(self):
        pass

    def migrate(self):
        pass

    def death(self):
        pass


class Herbivore(Animals):
    def __init__(self):
        pass

    def eat(self):
        pass


class Carnivore(Animals):
    def __init__(self):
        pass
