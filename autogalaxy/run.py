import os
import shutil
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autogalaxy_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"
NOTEBOOKS_NO_RUN = [
    "mask.ipynb",
    "light_centre.ipynb",
    "scaled_dataset.ipynb",
    "tutorial_5_model_fit.ipynb",
    "tutorial_3_hierarchical_models.ipynb",
    "tutorial_5_expectation_propagation.ipynb",
    "Zeus.ipynb",
    "EmceePlotter.ipynb",
    "tutorial_searches.ipynb",
    "example_0.ipynb",
    "example_1.ipynb",
    "wavelength_dependence.ipynb"  # Fix via https://github.com/Jammy2211/PyAutoGalaxy/issues/34
    "GetDist.ipynb",  # ' Breaks due to test_mode samples
    "tutorial_4_models.ipynb",  # Test mode generates invalid samples for quantile
    "tutorial_optional_manual.ipynb",  # Test mode generates invalid samples for quantile
]

def main():

    copy_tree(f"autogalaxy/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(WORKSPACE_PATH)
    build_util.execute_notebook("introduction.ipynb")

    if not os.path.exists(f"{WORKSPACE_PATH}/output"):
        os.mkdir(f"{WORKSPACE_PATH}/output")

    os.chdir(NOTEBOOKS_ROOT_PATH)

    for folder in [
        "howtogalaxy",
        "database"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
        )

    os.chdir(BUILD_PATH)
    copy_tree(f"autogalaxy/configs/test", f"{WORKSPACE_PATH}/config")

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
    copy_tree(f"autogalaxy/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)

    os.chdir(WORKSPACE_PATH)



if __name__ == "__main__":
    main()
