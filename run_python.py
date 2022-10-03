import os
import sys
import yaml

import build_util

os.environ["PYAUTOFIT_TEST_MODE"] = "1"

project = sys.argv[1]
folder = sys.argv[2]

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../{project}_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"

with open("no_run.yaml", "r+") as f:
    no_run_dict = yaml.load(f)

if __name__ == "__main__":

    build_util.execute_scripts_in_folder(
        workspace_path=WORKSPACE_PATH,
        folder=folder,
        root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
        no_run_list=no_run_dict[project],
    )