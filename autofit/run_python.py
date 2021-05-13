import os
import shutil
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"

SCRIPTS_NO_RUN = [
    "database.py",
    "graphical_models.py",
    "tutorial_2_graphical_model.py",
    "MultiNest.py",
    "UltraNest.py"

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

    os.chdir(SCRIPTS_ROOT_PATH)

    for folder in [
        "simulators",
        "howtofit",
        "overview",
        "features",
        "searches"
    ]:

        build_util.execute_scripts_in_folder(
            workspace_path=WORKSPACE_PATH,
            folder=folder,
            root_path=f"{SCRIPTS_ROOT_PATH}/{folder}",
            scripts_no_run=SCRIPTS_NO_RUN
        )

    os.chdir(BUILD_PATH)
    copy_tree(f"autofit/configs/default", f"{WORKSPACE_PATH}/config")
    os.chdir(WORKSPACE_PATH)
    os.system(f"git add -f config")
    os.chdir(BUILD_PATH)


if __name__ == "__main__":
    main()
