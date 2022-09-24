import os
import sys

import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autolens_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"
NOTEBOOKS_NO_RUN = [
    "mask.ipynb",
    "positions.ipynb",
    "lens_light_centre.ipynb",
    "scaled_dataset.ipynb",
    "pipeline.ipynb",
    "tutorial_6_model_fit.ipynb",
    "overview_10_clusters.ipynb",
    "tutorial_5_expectation_propagation.ipynb",
    "hyper_mode.ipynb",
    "Zeus.ipynb",
    "EmceePlotter.ipynb",
    "tutorial_searches.ipynb",
    "example_1.ipynb",
    "example_1.ipynb"
]

if __name__ == "__main__":
    folder = sys.argv[1]
    build_util.exexcute_notebooks_in_folder(
        ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
        NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
    )
