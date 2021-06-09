import os
import shutil
from distutils.dir_util import copy_tree
from . import build_util

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
    "tutorial_searches.ipynb",
    "hyper_mode.ipynb",
    "pipeline.ipynb",
    "light_parametric__mass_total__source_inversion.ipynb",
    "Emcee.ipynb",
    "PySwarms.ipynb",
    "Zeus.ipynb",
    "EmceePlotter.ipynb",
    "PySwarmsPlotter.ipynb",
    "ZeusPlotter.ipynb",
    "UltraNestPlotter.ipynb",
    "DynestyPlotter.ipynb",
]

def main():

    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(WORKSPACE_PATH)
    build_util.execute_notebook("introduction.ipynb")

    if os.path.exists(f"{WORKSPACE_PATH}/output"):
        try:
            os.rename(f"{WORKSPACE_PATH}/output", f"{WORKSPACE_PATH}/output_backup")
        except OSError:
            shutil.rmtree(f"{WORKSPACE_PATH}/output")

    if not os.path.exists(f"{WORKSPACE_PATH}/auto_files"):
        os.system("git clone https://github.com/Jammy2211/auto_files --depth 1")

    os.system(f"cp -r {WORKSPACE_PATH}/auto_files/autolens/output {WORKSPACE_PATH}")

    os.chdir(NOTEBOOKS_ROOT_PATH)

    for folder in [
        "howtolens",
    #   "database"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
        )

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/test", f"{WORKSPACE_PATH}/config")

    for folder in [
     #   "imaging",
     #   "interferometer",
     #   "point_source",
     #   "misc",
        "plot"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
        )

    shutil.rmtree(f"{WORKSPACE_PATH}/output")
    os.rename(f"{WORKSPACE_PATH}/output_backup", f"{WORKSPACE_PATH}/output")

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)

    os.chdir(WORKSPACE_PATH)
    shutil.rmtree("auto_files")


if __name__ == "__main__":
    main()
