#!/usr/bin/env python

import sys
import yaml
from pathlib import Path

import build_util

project = sys.argv[1]
directory = sys.argv[2]

CONFIG_PATH = Path(__file__).parent / "config"

with open(CONFIG_PATH / "no_run.yaml") as f:
    no_run_dict = yaml.safe_load(f)

if __name__ == "__main__":
    build_util.execute_scripts_in_folder(
        no_run_list=no_run_dict[project], directory=directory
    )
