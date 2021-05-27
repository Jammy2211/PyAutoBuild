import os
import shutil
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"

NOTEBOOKS_NO_RUN = [
    "database.ipynb",
    "graphical_models.ipynb",
    "tutorial_1_global_model.ipynb",
    "tutorial_2_graphical_model.ipynb",
    "MultiNest.ipynb",
    "UltraNest.ipynb"
]

def main():

    os.chdir(WORKSPACE_PATH)
 #   build_util.execute_notebook("introduction.ipynb")

    if os.path.exists(f"{WORKSPACE_PATH}/auto_files"):
        shutil.rmtree(f"{WORKSPACE_PATH}/auto_files")

    os.system("git clone https://github.com/Jammy2211/auto_files --depth 1")

    if os.path.exists(f"{WORKSPACE_PATH}/output/howtofit"):
        shutil.rmtree(f"{WORKSPACE_PATH}/output/howtofit")

    if os.path.exists(f"{WORKSPACE_PATH}/output/database.sqlite"):
        os.remove(f"{WORKSPACE_PATH}/output/database.sqlite")

    if os.path.exists(f"{WORKSPACE_PATH}/output/database_howtofit.sqlite"):
        os.remove(f"{WORKSPACE_PATH}/output/database_howtofit.sqlite")

    shutil.move("auto_files/autofit/output/howtofit", f"{WORKSPACE_PATH}/output")
    shutil.move("auto_files/autofit/output/database.sqlite", f"{WORKSPACE_PATH}/output")
    shutil.move("auto_files/autofit/output/database_howtofit.sqlite", f"{WORKSPACE_PATH}/output")

    shutil.rmtree("auto_files")

    os.chdir(BUILD_PATH)
    copy_tree(f"autofit/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(NOTEBOOKS_ROOT_PATH)

    for folder in [
        "simulators",
        "howtofit",
        "overview",
        "features",
        "searches"
    ]:

        build_util.exexcute_notebooks_in_folder(
            ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
            NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
        )

    os.chdir(BUILD_PATH)
    copy_tree(f"autofit/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)


if __name__ == "__main__":
    main()
