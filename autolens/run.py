import glob
import os
import re
import shutil
import subprocess
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
    "tutorial_3_lens_and_source.ipynb",
    "tutorial_4_x2_lens_galaxies.ipynb",
    "tutorial_5_complex_source.ipynb",
    "tutorial_8_model_fit.ipynb",
    "tutorial_6_model_fit.ipynb",
    "tutorial_2_samples.ipynb",
    "hyper_mode.ipynb",
    "pipeline.ipynb",
    "light_parametric__mass_total__source_inversion.ipynb",
    "non_linear_searches.ipynb"
]

def main():

    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(WORKSPACE_PATH)
    build_util.execute_notebook("introduction.ipynb")

  #  os.system("git clone https://github.com/Jammy2211/auto_files --depth 1")

    # if os.path.exists(f"{WORKSPACE_PATH}/output/database"):
    #     shutil.rmtree(f"{WORKSPACE_PATH}/output/database")
    #
    # shutil.move("auto_files/output/database", f"{WORKSPACE_PATH}/output")
    #
    # if os.path.exists(f"{WORKSPACE_PATH}/output/howtolens"):
    #     shutil.rmtree(f"{WORKSPACE_PATH}/output/howtolens")
    #
    # shutil.move("auto_files/output/howtolens", f"{WORKSPACE_PATH}/output")
    #
    # shutil.rmtree("auto_files")

    os.chdir(NOTEBOOKS_ROOT_PATH)

    for folder in [
    #    "howtolens",
        "database"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
        )

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/test", f"{WORKSPACE_PATH}/config")

    for folder in [
        "imaging",
        "interferometer",
        "point_source",
        "misc",
        "plot"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
        )

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)

if __name__ == "__main__":
    main()
