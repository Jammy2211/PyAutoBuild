import os
import shutil
import sys
from distutils.dir_util import copy_tree

import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autolens_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
SCRIPTS_NO_RUN = [
    "profiling.py",
    "overview_10_clusters.py",
    "tutorial_4_hierarchical_models.py",
    "tutorial_5_expectation_propagation.py",
    "Zeus.py",
    "EmceePlotter.py",
    "tutorial_searches.py",
    "example_0.py",
    "example_1.py",
    "wavelength_dependence.py"  # Fix via https://github.com/Jammy2211/PyAutoGalaxy/issues/34
    "GetDist.py",  # ' Breaks due to test_mode samples
    "tutorial_4_models.py",  # Test mode generates invalid samples for quantile
    "tutorial_optional_manual.py"  # Test mode generates invalid samples for quantile
]


def main():
    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(WORKSPACE_PATH)

    if not os.path.exists(f"{WORKSPACE_PATH}/output"):
        os.mkdir(f"{WORKSPACE_PATH}/output")

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/test", f"{WORKSPACE_PATH}/config")

    for folder in [
        "results",
        # "howtolens",
        # "overview",
        # "imaging",
        # "interferometer",
        # "multi",
        # "point_source",
        # "misc",
        # "plot"
    ]:

        build_util.execute_scripts_in_folder(
            workspace_path=WORKSPACE_PATH,
            folder=folder,
            root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
            scripts_no_run=SCRIPTS_NO_RUN,
        )

    shutil.rmtree(f"{WORKSPACE_PATH}/output")
    try:
        os.rename(f"{WORKSPACE_PATH}/output_backup", f"{WORKSPACE_PATH}/output")
    except FileNotFoundError:
        os.mkdir(f"{WORKSPACE_PATH}/output")

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)

    os.chdir(WORKSPACE_PATH)

    try:
        shutil.rmtree("auto_files")
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    folder = sys.argv[1]
    build_util.execute_scripts_in_folder(
        workspace_path=WORKSPACE_PATH,
        folder=folder,
        root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
        scripts_no_run=SCRIPTS_NO_RUN,
    )
