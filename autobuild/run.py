import os
from os import path
import sys
import yaml

import build_util

os.environ["PYAUTOFIT_TEST_MODE"] = "1"

project = sys.argv[1]
folder = sys.argv[2]

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../{project}_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
CONFIG_PATH = f"{BUILD_PATH}/autobuild/config"

with open(path.join(CONFIG_PATH, "no_run.yaml"), "r+") as f:
    no_run_dict = yaml.load(f)

if __name__ == "__main__":

    os.chdir(WORKSPACE_PATH)
    build_util.execute_notebook("introduction.ipynb")

    build_util.exexcute_notebooks_in_folder(
        ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
        no_run_list=no_run_dict[project],
    )