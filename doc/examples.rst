Examples
========

BioSim simulation
------------------

The BioSim simulation simulates the outcome of Rossumøya's ecosystem given
an Island map and an initial population. You can however add populations
mid-simulation as well as set both animal and landscape parameters yourself.

.. code-block:: python

    """
    Compatibility check for BioSim simulations.

    This script shall function with biosim packages written for
    the INF200 project January 2020.
    """

    plt.ion()

    geogr = """\
               OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)

    sim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
    sim.set_animal_parameters(
        "Carnivore",
        {
            "a_half": 70,
            "phi_age": 0.5,
            "omega": 0.3,
            "F": 65,
            "DeltaPhiMax": 9.0,
        },
    )
    sim.set_landscape_parameters("J", {"f_max": 700})

    sim.simulate(num_years=100, vis_years=1, img_years=2000)

    sim.add_population(population=ini_carns)
    sim.simulate(num_years=100, vis_years=1, img_years=2000)

    plt.savefig("check_sim.pdf")

    input("Press ENTER")


Population generator
--------------------

.. automodule:: examples.population_generator
    :inherited-members:

