import os
import shutil
from distutils.dir_util import copy_tree
from . import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"

NOTEBOOKS_NO_RUN = [
    "graphical_models.ipynb",
    "search_grid_search.ipynb",
    "search_chaining.ipynb",
    "sensitivity_mapping.ipynb",
    "tutorial_1_global_model.ipynb",
    "tutorial_2_graphical_model.ipynb",
    "tutorial_3_expectation_propagation.ipynb",
    "MultiNest.ipynb",
    "UltraNest.ipynb",
    "fit.ipynb", # timed out
]

def main():

    os.chdir(WORKSPACE_PATH)
 #   build_util.execute_notebook("introduction.ipynb")

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

    os.chdir(NOTEBOOKS_ROOT_PATH)

    for folder in [
        "../projects",
        "simulators",
        "howtofit",
        "overview",
        "features",
        "searches"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
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
