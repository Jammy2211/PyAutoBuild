import os
import shutil
from distutils.dir_util import copy_tree
import build_util

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

def main():

    os.chdir(WORKSPACE_PATH)

    if os.path.exists(f"{WORKSPACE_PATH}/output"):
        try:
            os.rename(f"{WORKSPACE_PATH}/output", f"{WORKSPACE_PATH}/output_backup")
        except OSError:
            shutil.rmtree(f"{WORKSPACE_PATH}/output")


    os.chdir(BUILD_PATH)
    copy_tree(f"autofit/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(SCRIPTS_ROOT_PATH)

    for folder in [
        "simulators",
        "howtofit",
        "overview",
        "features",
        "searches"
    ]:

        build_util.execute_scripts_in_folder(
            workspace_path=WORKSPACE_PATH,
            folder=folder,
            root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
            scripts_no_run=SCRIPTS_NO_RUN,
        )

    shutil.rmtree(f"{WORKSPACE_PATH}/output")
    os.rename(f"{WORKSPACE_PATH}/output_backup", f"{WORKSPACE_PATH}/output")

    os.chdir(BUILD_PATH)
    copy_tree(f"autofit/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)


if __name__ == "__main__":
    main()
