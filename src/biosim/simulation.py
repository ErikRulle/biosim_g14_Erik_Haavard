# -*- coding: utf-8 -*-

"""
"""

__author__ = "Erik Rullestad", "Håvard Molversmyr"
__email__ = "erikrull@nmbu.no", "havardmo@nmbu.no"


import biosim.island as bi
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class BioSim:
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
        self.herbivore_list = [self.island.total_island_population[0]]
        self.carnivore_list = [self.island.total_island_population[1]]
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        species.set_animal_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        landscape.set_landscape_parameters(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        for _ in range(num_years):
            new_island_population = self.island.annual_cycle()
            self.herbivore_list.append(new_island_population[0])
            self.carnivore_list.append(new_island_population[1])

            if num_years % vis_years == 0:
                pass


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
        animal_dict = {"Herbivores": self.island.total_island_population[0],
                       "Carnivore": self.island.total_island_population[1]}
        return animal_dict

    @property
    def animal_distribution(self):
        """
        Pandas DataFrame with animal count per species for each cell on island.
        """
        pandas_population = pd.DataFrame(self.island.population_in_each_cell,
                                         columns=["Herbivores", "Carnivores"])
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
            self._map_ax = self._fig.add_subplot(1, 2, 1)
            self._img_axis = None

        # Add right subplot for line graph of mean.
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(1, 2, 2)
            self._mean_ax.set_ylim(0, 0.02)

        # needs updating on subsequent calls to simulate()
        self._mean_ax.set_xlim(0, self._final_step + 1)

        if self._mean_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, self._final_step),
                                           np.full(self._final_step, np.nan))
            self._mean_line = mean_plot[0]
        else:
            xdata, ydata = self._mean_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_step)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._mean_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))

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
        plt.show()


    def plot_population_graph(self, year):
        """
        Plots the total herbivore and carnivore population for a given year.

        :param year: int, last year in simulation.
        """
        plt.plot(len(self.herbivore_list), self.herbivore_list)
        plt.plot(len(self.carnivore_list), self.carnivore_list)
        plt.legend(["Herbivores", "Carnivores"], loc="upper left")
        #plt.savefig







