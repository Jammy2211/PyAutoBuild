import os
from os import path
import sys
import yaml

import build_util

os.environ["PYAUTOFIT_TEST_MODE"] = "1"

project = sys.argv[1]
folder = sys.argv[2]

BUILD_PATH = os.getcwd()
CONFIG_PATH = f"{BUILD_PATH}/autobuild/config"

with open(path.join(CONFIG_PATH, "no_run.yaml"), "r+") as f:
    no_run_dict = yaml.load(f)

if __name__ == "__main__":

    build_util.execute_scripts_in_folder(
        folder=folder, root_path=folder, no_run_list=no_run_dict[project],
    )
