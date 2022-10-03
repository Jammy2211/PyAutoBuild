import os
import sys
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autocti_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
SCRIPTS_NO_RUN = [
    "x1_species_to_x2_species",
    "noise_scaling.py"
]

os.environ["PYAUTOFIT_TEST_MODE"] = "1"

if __name__ == "__main__":

    folder = sys.argv[1]

    build_util.execute_scripts_in_folder(
        workspace_path=WORKSPACE_PATH,
        folder=folder,
        root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
        scripts_no_run=SCRIPTS_NO_RUN,
    )