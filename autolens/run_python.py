import os
import shutil
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autolens_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
SCRIPTS_NO_RUN = [
    "mask.py",
    "positions.py",
    "lens_light_centre.py",
    "scaled_dataset.py",
    "tutorial_3_lens_and_source.py",
    "tutorial_4_x2_lens_galaxies.py",
    "tutorial_5_complex_source.py",
    "tutorial_8_model_fit.py",
    "tutorial_6_model_fit.py",
    "tutorial_searches.py",
    "tutorial_2_samples.py",
    "hyper_mode.py",
    "pipeline.py",
    "light_parametric__mass_total__source_inversion.py",
    "Emcee.py",
    "PySwarms.py",
    "Zeus.py",
    "EmceePlotter.py",
    "PySwarmsPlotter.py",
    "ZeusPlotter.py",
    "UltraNestPlotter.py",
    "DynestyPlotter.py",
]

def main():

    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(WORKSPACE_PATH)

    if os.path.exists(f"{WORKSPACE_PATH}/auto_files"):
        shutil.rmtree(f"{WORKSPACE_PATH}/auto_files")

    if os.path.exists(f"{WORKSPACE_PATH}/output"):
        try:
            os.rename(f"{WORKSPACE_PATH}/output", f"{WORKSPACE_PATH}/output_backup")
        except OSError:
            shutil.rmtree(f"{WORKSPACE_PATH}/output")

    os.system("git clone https://github.com/Jammy2211/auto_files --depth 1")

    if not os.path.exists(f"{WORKSPACE_PATH}/output"):
        os.mkdir(f"{WORKSPACE_PATH}/output")

    os.system(f"cp -r {WORKSPACE_PATH}/auto_files/autolens/output/howtolens {WORKSPACE_PATH}/output")
    shutil.move("auto_files/autolens/output/database.sqlite", f"{WORKSPACE_PATH}/output")

    shutil.rmtree("auto_files")

    os.chdir(SCRIPTS_ROOT_PATH)

    for folder in [
    #    "howtolens",
    #    "database"
    ]:

        build_util.execute_scripts_in_folder(
            workspace_path=WORKSPACE_PATH,
            folder=folder,
            root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
            scripts_no_run=SCRIPTS_NO_RUN
        )

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/test", f"{WORKSPACE_PATH}/config")

    for folder in [
      #  "imaging",
     #   "interferometer",
        "point_source",
        "misc",
        "plot"
    ]:

        build_util.execute_scripts_in_folder(
            workspace_path=WORKSPACE_PATH,
            folder=folder,
            root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
            scripts_no_run=SCRIPTS_NO_RUN
        )

    shutil.rmtree(f"{WORKSPACE_PATH}/output")
    os.rename(f"{WORKSPACE_PATH}/output_backup", f"{WORKSPACE_PATH}/output")

    os.chdir(BUILD_PATH)
    copy_tree(f"autolens/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)


if __name__ == "__main__":
    main()
