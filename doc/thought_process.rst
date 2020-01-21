Our thought process for solving the task
========================================

    *"Give me six hours to chop down a tree and I will spend the first four
    sharpening the axe!"*

    \- Abraham Lincoln

When given this task, we sat down with pen and paper to get an overview of the
task itself, and to brainstorm possible ways to solve it as best we could
given our programming experience and abilities.

Structure
---------
We quickly understood the need for the generic class ``Island``, as well as
the generic superclasses ``Landscape`` and ``Animal``, so we created these
classes in different modules. Within each of these modules we could then focus
on what methods to implement, and whether or not the methods in question
should be implemented in the superclass or in a subclass. We ended up with
several subclasses, one for each landscape type, i.e. ``Jungle``, ``Savannah``,
``Desert``. ``Mountain`` and ``Ocean``, as well as a subclass for the two
different animal species on the island, resulting in the subclasses,
``Herbivore`` and ``Carnivore``. For a complete overview of our structure and
method implementation, see the :ref:`API Reference`.






