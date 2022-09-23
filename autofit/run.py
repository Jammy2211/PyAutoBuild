import os
import sys

import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"

NOTEBOOKS_NO_RUN = [
    "graphical_models.ipynb",
    "search_grid_search.ipynb",
    "sensitivity_mapping.ipynb",
    "tutorial_4_data_and_models.ipynb",
    "tutorial_5_expectation_propagation.ipynb",
    "UltraNest.ipynb",
]

if __name__ == "__main__":
    folder = sys.argv[1]
    build_util.exexcute_notebooks_in_folder(
        ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
        NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
    )
