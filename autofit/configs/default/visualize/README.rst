The visualize config files contain the default settings used by visualization in **PyAutoFit**. The majority of
config files are described in the ``autofit_workspace/plot`` package.

The *general.ini* config contains the following sections and variables:

[general]
    backend
        The matploblib backend used for visualization (see
        https://gist.github.com/CMCDragonkai/4e9464d9f32f5893d837f3de2c43daa4 for a description of backends).

        If you use an invalid backend for your computer, **PyAutoLens** may crash without an error or reset your machine.
        The following backends have worked for **PyAutoLens** users:

        TKAgg (default)

        Qt5Agg (works on new MACS)

        Qt4Agg

        WXAgg

        WX

        Agg (outputs to .fits / .png but doesn't'display figures during a run on your computer screen)


The ``plots_search.ini`` config file customizes every image associated with the non-linear search that is output to
hard-disk during a model-fit.

For example, if in the [dynesty] section ``cornerplot=True``, the ``cornerplot.png`` subplot file will be plotted
every time visualization is performed.