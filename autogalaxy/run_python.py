import os
import shutil
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autogalaxy_workspace"
WORKSPACE_TEST_PATH = f"{os.getcwd()}/../autogalaxy_workspace_test"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
SCRIPTS_NO_RUN = [
    "mask.py",
    "light_centre.py",
    "scaled_dataset.py",
    "profiling.py",
    "tutorial_4_hierarchical_models.py",
    "tutorial_5_expectation_propagation.py",
    "Zeus.py",
    "EmceePlotter.py",
    "tutorial_searches.py",
    "example_0.py",
    "example_1.py",
    "wavelength_dependence.py" # Fix via https://github.com/Jammy2211/PyAutoGalaxy/issues/34
    "GetDist.py", # ' Breaks due to test_mode samples
]

def main():

    copy_tree(f"autogalaxy/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(WORKSPACE_PATH)

    if not os.path.exists(f"{WORKSPACE_PATH}/output"):
        os.mkdir(f"{WORKSPACE_PATH}/output")

    os.chdir(SCRIPTS_ROOT_PATH)

    for folder in [
  #      "results"
    ]:

        build_util.execute_scripts_in_folder(
            workspace_path=WORKSPACE_PATH,
            folder=folder,
            root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
            scripts_no_run=SCRIPTS_NO_RUN
       )

    os.chdir(BUILD_PATH)
    copy_tree(f"autogalaxy/configs/test", f"{WORKSPACE_PATH}/config")

    for folder in [
     #     "howtogalaxy",
    #     "overview",
      #   "imaging",
     #    "interferometer",
         "multi",
         "misc",
         "plot"
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
    copy_tree(f"autogalaxy/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)

    os.chdir(WORKSPACE_TEST_PATH)

    build_util.execute_script(os.path.join("imaging", "visualizer.py"))
    build_util.execute_script(os.path.join("interferometer", "visualizer.py"))

    os.chdir(WORKSPACE_PATH)


if __name__ == "__main__":
    main()
