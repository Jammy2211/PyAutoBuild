import os
import sys

import build_util

os.environ["PYAUTOFIT_TEST_MODE"] = "1"

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"

SCRIPTS_NO_RUN = [
    "search_grid_search.py",
    "graphical_models.py",
    "sensitivity_mapping.py",
    "tutorial_4_data_and_models.py",
    "tutorial_5_expectation_propagation.py",
    "UltraNest.py",
]


if __name__ == "__main__":
    folder = sys.argv[1]

    build_util.execute_scripts_in_folder(
        workspace_path=WORKSPACE_PATH,
        folder=folder,
        root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
        scripts_no_run=SCRIPTS_NO_RUN,
    )
