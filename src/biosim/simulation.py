# -*- coding: utf-8 -*-

"""
:mod:`biosim.simulation` defines the BioSim class interface for simulation of
Rossumøya's ecosystem.
"""

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import biosim.island as bi
import biosim.landscape as bl
import biosim.animals as ba


class BioSim:
    """
    This class generates the outline for the simulation of Rossumøya's
    ecosystem, with visualisation.
    """
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
        animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
        densities
        :param img_base: String with beginning of file name for figures,
        including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        random.seed(seed)
        self.last_year_simulated = 0
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.island = bi.Island(island_map=island_map)
        self.island.populate_the_island(ini_pop)
        self.herbivore_list = [self.island.total_species_population[0]]
        self.carnivore_list = [self.island.total_species_population[1]]
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt
        self._img_ctr = 0

        # the following will be initialized by setup_graphics
        self._fig = None
        self._map_ax = None
        self._map_axis = None
        self._pop_ax = None
        self._pop_axis = None
        self._herb_heat_ax = None
        self._herb_heat_axis = None
        self._carn_heat_ax = None
        self._carn_heat_axis = None

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            ba.Herbivore.set_animal_parameters(params)
        elif species == "Carnivore":
            ba.Carnivore.set_animal_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == "J":
            bl.Jungle.set_landscape_parameters(params)
        elif landscape == "S":
            bl.Savannah.set_landscape_parameters(params)
        elif landscape == "D":
            bl.Desert.set_landscape_parameters(params)
        elif landscape == "M":
            bl.Mountain.set_landscape_parameters(params)
        elif landscape == "O":
            bl.Ocean.set_landscape_parameters(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self.setup_graphics()

        for _ in range(num_years):
            new_island_population = self.island.annual_cycle()
            self.herbivore_list.append(new_island_population[0])
            self.carnivore_list.append(new_island_population[1])

            if num_years % vis_years == 0:
                self.update_graphics()

            if num_years % img_years == 0:
                self.save_graphics()

            self.last_year_simulated += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.populate_the_island(population)

    @property
    def year(self):
        """
        Last year simulated.
        """
        return self.last_year_simulated

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        """
        return self.herbivore_list[-1] + self.carnivore_list[-1]

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        """
        animal_dict = {"Herbivore": self.island.total_species_population[0],
                       "Carnivore": self.island.total_species_population[1]}
        return animal_dict

    @property
    def animal_distribution(self):
        """
        Pandas DataFrame with animal count per species for each cell on island.
        """
        pandas_population = pd.DataFrame(
            self.island.population_in_each_cell,
            columns=["Row", "Col", "Herbivore", "Carnivore"])
        return pandas_population

    def make_movie(self):
        """
        Create MPEG4 movie from visualization images saved.
        """

    def setup_graphics(self):
        """

        """
        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 2, 1)
            self._map_axis = None

        # Add right subplot for line graph of mean.
        if self._pop_ax is None:
            self._pop_ax = self._fig.add_subplot(2, 2, 2)
            if self.ymax_animals is not None:
                self._pop_ax.set_ylim(0, self.ymax_animals)

        if self._herb_heat_ax is None:
            self._herb_heat_ax = self._fig.add_subplot(2, 2, 3)

        if self._carn_heat_ax is None:
            self._carn_heat_ax = self._fig.add_subplot(2, 2, 4)

    def plot_island_map(self):
        """
        Creates a map plot of the input island map string.
        """
        #                   R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in self.island.string_map]

        fig = plt.figure()

        axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        axim.imshow(map_rgb)
        axim.set_xticks(range(len(map_rgb[0])))
        axim.set_xticklabels(range(0, 1 + len(map_rgb[0])))
        axim.set_yticks(range(len(map_rgb)))
        axim.set_yticklabels(range(0, 1 + len(map_rgb)))

        axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                   'Savannah', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

        #axim.grid()
        #plt.show()
        #plt.savefig("src/biosim/images/Rossumøya.png")

    def plot_population_graph(self):
        """
        Plots the total herbivore and carnivore population for a given year.

        :param year: int, last year in simulation.
        """
        if self._pop_axis is None:
            self._pop_axis = plt.plot(len(self.herbivore_list),
                                      self.herbivore_list)
            self._pop_axis.plot(len(self.carnivore_list), self.carnivore_list)
            self._pop_axis.legend(
                ["Herbivores", "Carnivores"], loc="upper left")

    def plot_heatmap(self):
        """

        """
        df = self.animal_distribution
        herbivore_array = df.pivot_table(
            columns="Col", index="Row", values="Herbivore")
        carnivore_array = df.pivot_table(
            columns="Col", index="Row", values="Carnivore")

        if self._herb_heat_axis is None:
            self._herb_heat_axis = plt.imshow(
                herbivore_array, cmap="BuGn",
                interpolation="nearest", vmax=self.cmax_animals)
            self._herb_heat_axis.colorbar()

        if self._carn_heat_axis is None:
            self._carn_heat_axis = plt.imshow(
                carnivore_array, cmap="OrRd",
                interpolation="nearest",
                vmax=self.cmax_animals)
            self._carn_heat_axis.colorbar()

    def update_graphics(self):
        """

        """
        self.plot_population_graph()
        self.plot_heatmap()
        plt.pause(1e-3)

    def save_graphics(self):
        """

        """
        if self.img_base is None:
            return

        plt.savefig(f"{self.img_base}_{self._img_ctr:05d}.{self.img_fmt}")

        self._img_ctr += 1