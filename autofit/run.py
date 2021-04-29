import glob
import os
import re
import shutil
import subprocess
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"

NOTEBOOKS_NO_RUN = [
    "tutorial_2_graphical_model.ipynb",
    "tutorial_2_aggregator.ipynb",
    "tutorial_3_querying.ipynb",
    "tutorial_4_data_and_models.ipynb",
    "graphical_models.ipynb",
    "MultiNest.ipynb"
]

def main():

    # os.chdir(WORKSPACE_PATH)
    # build_util.execute_notebook("introduction.ipynb")

    # os.system("git clone https://github.com/Jammy2211/auto_files --depth 1")
    #
    # if os.path.exists(f"{WORKSPACE_PATH}/output/howtofit"):
    #     shutil.rmtree(f"{WORKSPACE_PATH}/output/howtofit")
    #
    # shutil.move("auto_files/output/howtofit", f"{WORKSPACE_PATH}/output")
    # shutil.rmtree("auto_files")

    copy_tree(f"autofit/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(NOTEBOOKS_ROOT_PATH)

    for folder in [
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

    os.chdir(BUILD_PATH)
    copy_tree(f"autofit/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)


if __name__ == "__main__":
    main()
