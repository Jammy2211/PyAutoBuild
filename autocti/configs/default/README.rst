The ``config`` folder contains configuration files which customize default **PyAutoLens**.

Folders
-------

- ``grids``: Configs for default behaviour of grids when used for ray-tracing.
- ``non-linear``: Configs for default non-linear search (e.g. MCMC, nested sampling) settings.
- ``notation``: Configs defining labels and formatting of model parameters when used for visualization.
- ``priors``: Configs defining default priors assumed on every lens model component and set of parameters.
- ``visualize``: Configs defining what images are output by a lens model fit.

Files
-----

- ``general.ini``: Customizes general **PyAutoLens** settings.
- ``logging.yaml``: Customizes the logging behaviour of **PyAutoLens**.


The **general.ini** contains the following sections and variables:

[output]
    log_to_file
        If True the outputs of processes like the non-linear search are logged to a file (and not printed to screen).
    log_file
        The file name the logged output is written to (in the non-linear search output folder).
    log_level
        The level of logging.
    model_results_decimal_places
        The number of decimal places the estimated values and errors of all parameters in the model.results file are
        output to.
    info_whitespace_length
        The length of whitespace between the parameter names and priors / inferred values in the ``model.info`` and
        ``result.info`` attributes (this is also reflected in the ``model.info`` / ``model.results`` files.
    remove_files
        If True, all output files of a non-linear search (e.g. samples, samples_backup, model.results, images, etc.)
        are deleted once the model-fit has completed.

        A .zip file of all output is always created before files are removed, thus results are not lost with this
        option turned on. If PyAutoLens does not find the output files of a model-fit (because they were removed) but
        does find this .zip file, it will unzip the contents and continue the analysis as if the files were
        there all along.

        This feature was implemented because super-computers often have a limit on the number of files allowed per
        user and the large number of files output by PyAutoLens can exceed this limit. By removing files the
        number of files is restricted only to the .zip files.
    force_pickle_overwrite
        A model-fit outputs pickled files of the model, search, results, etc., which the database feature can load.
        If this setting it ``True`` these pickle files are recreated when a new model-fit is performed, even if
        the search is complete.

The following setting flips all images that are loaded by **PyAutoLens** so that they appear the same orinetation as
the software ds9:

[fits]
    flip_for_ds9
        If ``True``, the ndarray of all .fits files containing an image, noise-map, psf, etc, is flipped upside down
        so its orientation is the same as ds9.

The following settings are specific for High Performance Super computer use with **PyAutoLens**.

[hpc]
    hpc_mode
        If ``True``, HPC mode is activated, which disables GUI visualization, logging to screen and other settings which
        are not suited to running on a super computer.
    iterations_per_update
        The number of iterations between every update (visualization, results output, etc) in HPC mode, which may be
        better suited to being less frequent on a super computer.

The following settings customize how a model is handled by **PyAutoFit**:

[model]
    ignore_prior_limits
        If ``True`` the limits applied to priors will be ignored, where limits set upper / lower limits. This should be
        disabled if one has difficult manipulating results in the database due to a ``PriorLimitException``.

The library `numba <https://github.com/numba/numba>`_ is used to speed up functions, by converting them to C callable
functions before the Python interpreter runs:

[numba]
    nopython
        If True, functions which hve a numba decorator must not convert back to Python during a run and thus must stay
        100% C. All PyAutoLens functions were developed with nopython mode turned on.
    cache
        If True, the C version of numba functions are cached on the hard-disk so they do not need to be
        recompiled every time **PyAutoLens** is rerun. If False, the first time every function is run will have a small
        delay (0.1-1.0 seconds) as it has to be numba compiled again.
    parallel
        If True, all functions decorated with the numba.jit are run with parallel processing on.

[inversion]
    interpolated_grid_shape {image_grid, source_grid}
        In order to output inversion reconstructions (which could be on a Voronoi grid) to a .fits file, the
        reconstruction is interpolated to a square grid of pixels. This option determines this grid:

        image_grid: The interpolated grid is the same shape, resolution and centering as the observed image-data.

        source_grid: The interpolated grid is zoomed to over-lay the source-plane reconstructed source and uses
        dimensions derived from the number of pixels used by the reconstruction.

[hyper]
    hyper_minimum_percent : float
        When creating hyper-images (see howtolens/chapter_5) all flux values below a certain value are rounded up an input
        value. This prevents negative flux values negatively impacting hyper-mode features or zeros creating division
        by zero errors.

        The value pixels are rounded to are the maximum flux value in the hyper image multipled by an input percentage
        value.

        The minimum percentage value the hyper image is mulitpled by in order to determine the value fluxes are rounded
        up to.
    hyper_noise_limit : float
        When noise scaling is activated (E.g. via hyper galaxies) this value is the highest value a noise value can
        numerically be scaled up too. This prevents extremely large noise map values creating numerically unstable
        log likelihood values.
    stochastic_outputs
        If ``True``, information on the stochastic likelihood behaviour of any KMeans based pixelization is output.

[profiling]
    should_profile
        If ``True`` the ``profile_log_likelihood_function()`` function of an analysis class is called throughout a model-fit.
    repeats
        The number of repeat function calls used to measure run-times.
    parallel_profile
        If ``True`` the parallelization of the fit is profiled outputting a cPython graph.

[analysis]
    n_cores
        The number of cores a parallelized Analysis class uses by default.

[test]
    test_mode
        If ``True`` this disables sampling of a search to provide a solution in one iteration. It is used for testing
        **PyAutoLens**.