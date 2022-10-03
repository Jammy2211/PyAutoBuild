import os
import sys
import build_util

os.environ["PYAUTOFIT_TEST_MODE"] = "1"

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
    "tutorial_4_models.py", # Test mode generates invalid samples for quantile
    "tutorial_optional_manual.py" # Test mode generates invalid samples for quantile
]

if __name__ == "__main__":

    folder = sys.argv[1]

    build_util.execute_scripts_in_folder(
        workspace_path=WORKSPACE_PATH,
        folder=folder,
        root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
        scripts_no_run=SCRIPTS_NO_RUN,
    )
