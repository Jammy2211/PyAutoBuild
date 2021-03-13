import glob
import os
import re
import shutil
import subprocess
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autolens_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"


def main():

    if os.path.exists(f"{WORKSPACE_PATH}/config_temp"):
        shutil.rmtree(f"{WORKSPACE_PATH}/config_temp")
    os.rename(f"{WORKSPACE_PATH}/config", f"{WORKSPACE_PATH}/config_temp")
    os.mkdir(f"{WORKSPACE_PATH}/config")
    copy_tree("autolens_workspace_config", f"{WORKSPACE_PATH}/config")

    os.system("git clone https://github.com/Jammy2211/auto_files --depth 1")

    if os.path.exists(f"{WORKSPACE_PATH}/output/database"):
        shutil.rmtree(f"{WORKSPACE_PATH}/output/database")

    shutil.move("auto_files/output/database", f"{WORKSPACE_PATH}/output")

    if os.path.exists(f"{WORKSPACE_PATH}/output/howtolens"):
        shutil.rmtree(f"{WORKSPACE_PATH}/output/howtolens")

    shutil.move("auto_files/output/howtolens", f"{WORKSPACE_PATH}/output")

    shutil.rmtree("auto_files")

    os.chdir(WORKSPACE_PATH)
    build_util.execute_notebook("introduction.ipynb")

    os.chdir(NOTEBOOKS_ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"

        if "gui" not in notebooks_path:

            os.chdir(notebooks_path)
            for f in glob.glob(f"*.ipynb"):
                build_util.execute_notebook(f)

    shutil.rmtree(f"{WORKSPACE_PATH}/config")
    os.rename(f"{WORKSPACE_PATH}/config_temp", f"{WORKSPACE_PATH}/config")


if __name__ == "__main__":
    main()
