import json
import os
import sys

import build_util

os.environ["PYAUTOFIT_TEST_MODE"] = "1"

project = sys.argv[1]
folder = sys.argv[2]

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../{project}_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"


if __name__ == "__main__":

    with open("scripts_no_run.json", "r+") as f:
        scripts_no_run_dict = json.load(f)

    build_util.execute_scripts_in_folder(
        workspace_path=WORKSPACE_PATH,
        folder=folder,
        root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
        scripts_no_run=scripts_no_run_dict[project],
    )