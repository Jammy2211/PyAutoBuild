Config files which specify the default matplotlib settings when figures and subplots are plotted.

For example, the ``Figure.ini`` config file has the following lines:

.. code-block:: bash

    [figure]
    figsize=(7, 7)
    aspect=square

    [subplot]
    figsize=auto
    aspect=square

This means that when a figure (e.g. a single image) is plotted it will use ``figsize=(7,7)`` and ``aspect="square`` if
the values of these parameters are not manually set by the user via the ``mat_plot_2d``.

Subplots (e.g. more than one image) will always use ``figsize="auto`` by default.

These configuration files can be customized such that the appearance of figures and subplots for a user is optimal for
your computer set up.

Examples
--------
Example scripts using all of the plot objects which have corresponding configuration files here are given at
`autolens_workspace.plot`.

Files
-----

EinsteinRadiusAXVLine.ini
    Customizes the appearance of a 1D line (plotted via ``plt.axvline()``)showing the Einstein radius on 1D plots of mass quantities.

ArrayOverlay.ini
    Customizes the appearance of 2D array overlaps plotted via``plt.imshow()``.
BorderScatter.ini
    Customizes the appearance of the 2D mask border plotted via ``plt.scatter()``.
CausticsPlot.ini
    Customizes the appearance of 2D caustics plotted via ``plt.plot()``.
CriticalCurvesPlot.ini
    Customizes the appearance of 2D critical curves plotted via ``plt.plot()``.
GridPlot.ini
    Customizes the appearance of any 2D grid plotted via ``plt.plot()``.
GridScatter.ini
    Customizes the appearance of any 2D grid plotted via ``plt.scatter()``.
IndexScatter.ini
    Customizes the appearance of 2D mapper indexes plotted via ``plt.scatter()``.
LightProfileCentresScatter.ini
    Customizes the appearance of the light profile centres plotted in 2D via ``plt.scatter()``.
MaskScatter.ini
    Customizes the appearance of the 2D mask plotted via ``plt.scatter()``.
MassProfileCentresScatter.ini
    Customizes the appearance of the mass profile centres plotted in 2D via ``plt.scatter()``.
MultipleImagesCentresScatter.ini
    Customizes the appearance of multiple images plotted in 2D via ``plt.scatter()``.
OriginScatter.ini
    Customizes the appearance of the 2D grid (y,x) origin plotted via ``plt.scatter()``.
PatchOverlay.ini
    Customizes the appearance of patches plotted over figures using the matplolit ``patch`` methods.
PositionsScatter.ini
    Customizes the appearance of positions plotted in 2D via ``plt.scatter()``.
VectorQuiver.ini
    Customizes the appearance of vectors plotted 2D via ```plt.quiver()``.
VoronoiDrawer.ini
    Customizes the appearance of Voronoi diagrams plotted via ```plt.fill()``.