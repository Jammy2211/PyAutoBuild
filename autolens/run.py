import os
import shutil
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autolens_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"
NOTEBOOKS_NO_RUN = [
    "mask.ipynb",
    "positions.ipynb",
    "lens_light_centre.ipynb",
    "scaled_dataset.ipynb",
    "pipeline.ipynb",
    "tutorial_6_model_fit.ipynb",
    "overview_10_clusters.ipynb",
    "tutorial_5_expectation_propagation.ipynb",
    "hyper_mode.ipynb",
    "Zeus.ipynb",
    "EmceePlotter.ipynb",
    "tutorial_searches.ipynb",
    "example_1.ipynb",
    "example_1.ipynb"
]

def main():

    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(WORKSPACE_PATH)
    build_util.execute_notebook("introduction.ipynb")


    if not os.path.exists(f"{WORKSPACE_PATH}/output"):
        os.mkdir(f"{WORKSPACE_PATH}/output")

 #   os.system(f"cp -r {WORKSPACE_PATH}/auto_files/autolens/output {WORKSPACE_PATH}")

    os.chdir(NOTEBOOKS_ROOT_PATH)

    for folder in [
        "howtolens",
        "database"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
        )

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/test", f"{WORKSPACE_PATH}/config")

    for folder in [
        "overview",
        "imaging",
        "interferometer",
        "multi",
        "point_source",
        "misc",
        "plot"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
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
    main()
