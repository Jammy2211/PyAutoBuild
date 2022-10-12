import os
import sys

import build_util

project = sys.argv[1]
folder = sys.argv[2]

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../{project}_workspace_test"
BUILD_ROOT_PATH = f"{WORKSPACE_PATH}/build"
CONFIG_PATH = f"{BUILD_PATH}/autobuild/config"

if __name__ == "__main__":

    build_util.execute_scripts_in_folder(
        workspace_path=WORKSPACE_PATH,
        folder=folder,
        root_path=f"{BUILD_ROOT_PATH}/{folder}",
    )