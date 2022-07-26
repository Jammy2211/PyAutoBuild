The visualize config files contain the default settings used by visualization in **PyAutoGalaxy**. The majority of
config files are described in the ``autogalaxy_workspace/plot`` package.

The *general.ini* config contains the following sections and variables:

[general]
    backend
        The matploblib backend used for visualization (see
        https://gist.github.com/CMCDragonkai/4e9464d9f32f5893d837f3de2c43daa4 for a description of backends).

        If you use an invalid backend for your computer, **PyAutoGalaxy** may crash without an error or reset your machine.
        The following backends have worked for **PyAutoGalaxy** users:

        TKAgg (default)

        Qt5Agg (works on new MACS)

        Qt4Agg

        WXAgg

        WX

        Agg (outputs to .fits / .png but doesn't'display figures during a run on your computer screen)

    in_kpc
        If ``True`` the x and y axis of 1D and 2D figures are plotted in kpc instead of arcseconds.


The ``include.ini`` config file customizes every feature that appears on plotted images by default (e.g. crtiical
curves, a mask, light profile centres, etc.).

For example, if in the [include_2d] section ``mask=False``, the mask will not be plotted on any applicable figure
by default.


The ``plots.ini`` config file customizes every image that is output to hard-disk during a model-fit.

For example, if in the [fit] section ``subplot_fit=True``, the ``fit_imaging.png`` subplot file will be plotted
every time visualization is performed.


The ``plots_search.ini`` config file customizes every image associated with the non-linear search that is output to
hard-disk during a model-fit.

For example, if in the [dynesty] section ``cornerplot=True``, the ``cornerplot.png`` subplot file will be plotted
every time visualization is performed.