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
SCRIPTS_FOLDER_NAME = os.environ.get("SCRIPTS_FOLDER_NAME", "scripts")
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/${SCRIPTS_FOLDER_NAME}"
CONFIG_PATH = f"{BUILD_PATH}/autobuild/config"

with open(path.join(CONFIG_PATH, "no_run.yaml"), "r+") as f:
    no_run_dict = yaml.load(f)

if __name__ == "__main__":

    build_util.execute_scripts_in_folder(
        workspace_path=WORKSPACE_PATH,
        folder=folder,
        root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
        no_run_list=no_run_dict[project],
    )
