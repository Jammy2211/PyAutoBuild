import os
from os import path
import sys
from pathlib import Path

import yaml

import build_util

os.environ["PYAUTOFIT_TEST_MODE"] = "1"

project = sys.argv[1]
folder = sys.argv[2]

CONFIG_PATH = Path(__file__).parent / "config"

with open(CONFIG_PATH / "no_run.yaml") as f:
    no_run_dict = yaml.load(f)

if __name__ == "__main__":

    build_util.execute_scripts_in_folder(
        folder=folder, root_path=folder, no_run_list=no_run_dict[project],
    )
