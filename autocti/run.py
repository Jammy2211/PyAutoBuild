import os
import shutil
from distutils.dir_util import copy_tree
import build_util

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autocti_workspace"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"
NOTEBOOKS_NO_RUN = ["noise_scaling.ipynb"]

def main():

    copy_tree(f"autocti/configs/default", f"{WORKSPACE_PATH}/config")

    os.chdir(WORKSPACE_PATH)
    build_util.execute_notebook("introduction.ipynb")

    if not os.path.exists(f"{WORKSPACE_PATH}/output"):
        os.mkdir(f"{WORKSPACE_PATH}/output")

    os.chdir(NOTEBOOKS_ROOT_PATH)

    # for folder in []:
    #
    #     build_util.exexcute_notebooks_in_folder(
    #         ROOT_PATH=f"{NOTEBOOKS_ROOT_PATH}/{folder}",
    #         NOTEBOOKS_NO_RUN=NOTEBOOKS_NO_RUN
    #     )

    os.chdir(BUILD_PATH)
    copy_tree(f"autocti/configs/test", f"{WORKSPACE_PATH}/config")

    for folder in [
        "imaging_ci",
        "line",
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
    copy_tree(f"autocti/configs/default", f"{WORKSPACE_PATH}/config")
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
