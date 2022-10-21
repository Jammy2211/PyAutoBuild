import os
from os import path
import glob
import shutil
import sys
from pathlib import Path

import yaml

import build_util
import generate_autofit

WORKSPACE_PATH = Path.cwd()
CONFIG_PATH = WORKSPACE_PATH.parent / "PyAutoBuild/autobuild/config"

project = WORKSPACE_PATH.name

with open(path.join(CONFIG_PATH, "copy_files.yaml"), "r+") as f:
    copy_files_dict = yaml.load(f)

copy_files_list = copy_files_dict[project]


def is_copy_file(file_path):
    return any(copy_file in str(file_path) for copy_file in copy_files_list)


if __name__ == "__main__":
    generate_autofit.generate_project_folders()

    for scripts_path in map(Path, glob.glob(f"{WORKSPACE_PATH}/scripts/*/")):
        notebooks_path = scripts_path.parent.parent / "notebooks" / scripts_path.name

        print(f"{scripts_path} -> {notebooks_path}")
        os.makedirs(notebooks_path, exist_ok=True)

        for notebook_path in glob.glob(f"{notebooks_path}/*.ipynb*"):
            os.remove(notebook_path)

        for script_path in map(Path, glob.glob(f"{scripts_path}/*.py")):
            if script_path.name == "__init__.py":
                continue
            if is_copy_file(script_path):
                source_path = script_path
                target_path = notebooks_path / script_path.name
            else:
                source_path = build_util.py_to_notebook(script_path)
                target_path = notebooks_path / source_path.name

            shutil.move(source_path, target_path)
            os.system(f"git add -f {target_path}")

        for read_me_path in map(Path, glob.glob(f"{scripts_path}/*.rst")):
            target_path = notebooks_path / read_me_path.name
            shutil.copy(read_me_path, target_path)
            os.system(f"git add -f {target_path}")
