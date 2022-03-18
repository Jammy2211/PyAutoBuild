import os
import shutil
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"

SCRIPTS_NO_RUN = [
    "search_grid_search.py",
    "tutorial_1_global_model.py",
    "tutorial_2_graphical_model.py",
    "tutorial_3_expectation_propagation.py",
    "tutorial_4_hierachical.py",
    "tutorial_4_data_and_models.py",
    "graphical_models.py",
    "sensitivity_mapping.py",
    "MultiNest.py",
    "UltraNest.py",
]

def main():

    os.chdir(WORKSPACE_PATH)

    if os.path.exists(f"{WORKSPACE_PATH}/output"):
        try:
            os.rename(f"{WORKSPACE_PATH}/output", f"{WORKSPACE_PATH}/output_backup")
        except OSError:
            shutil.rmtree(f"{WORKSPACE_PATH}/output")

    if not os.path.exists(f"{WORKSPACE_PATH}/auto_files"):
        os.system("git clone https://github.com/Jammy2211/auto_files --depth 1")

    os.system(f"cp -r {WORKSPACE_PATH}/auto_files/autofit/output {WORKSPACE_PATH}")

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
            scripts_no_run=SCRIPTS_NO_RUN
        )

    shutil.rmtree(f"{WORKSPACE_PATH}/output")
    os.rename(f"{WORKSPACE_PATH}/output_backup", f"{WORKSPACE_PATH}/output")

    os.chdir(BUILD_PATH)
    copy_tree(f"autofit/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)

    os.chdir(WORKSPACE_PATH)
    shutil.rmtree("auto_files")


if __name__ == "__main__":
    main()
