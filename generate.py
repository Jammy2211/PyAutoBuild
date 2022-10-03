import os
import glob
import shutil
import yaml

import build_util
import generate_autofit

project = sys.argv[1]
folder = sys.argv[2]

BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../{project}_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"

with open("copy_files.yaml", "r+") as f:
    copy_files_dict = yaml.load(f)

copy_files_list = copy_files_dict[project]

with open("notebooks_remove.yaml", "r+") as f:
    notebooks_remove_dict = yaml.load(f)

notebooks_remove_list = notebooks_remove_dict[project]


if __name__ == "__main__":

    if project == "autofit":
        generate_autofit.generate_project_folders()

    os.chdir(SCRIPTS_ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:

        scripts_path = f"{SCRIPTS_ROOT_PATH}/{x}"
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"
        if "__pycache__" in x:
            continue
        print(f"Processing dir <{x}>, {scripts_path} -> {notebooks_path}")

        ### Remove Old notebooks ###

        for f in glob.glob(f"{notebooks_path}/*.ipynb"):
            os.remove(f)
        for f in glob.glob(f"{notebooks_path}/*.ipynb_checkpoints"):
            shutil.rmtree(f)


        ### Convert ###

        os.chdir(scripts_path)
        for f in glob.glob(f"*.py"):
            build_util.py_to_notebook(f)

        for f in glob.glob(f"*.ipynb"):
            build_util.uncomment_jupyter_magic(f)


        ### Copy notebooks to notebooks folder ###

        for f in glob.glob(f"*.ipynb"):
            os.makedirs(f"{notebooks_path}", exist_ok=True)
            shutil.move(f"{scripts_path}/{f}", f"{notebooks_path}/{f}")
            os.system(f"git add -f {notebooks_path}/{f}")
        if os.path.exists(f"{notebooks_path}/__init__.ipynb"):
            os.remove(f"{notebooks_path}/__init__.ipynb")


        ### Copy README.rst files ###

        for f in glob.glob(f"*.rst"):
            shutil.copy(f"{scripts_path}/{f}", f"{notebooks_path}/{f}")
            os.system(f"git add -f {notebooks_path}/{f}")


    ### Copy specific Python Files ###

    for x in copy_files_list:
        scripts_path = f"{SCRIPTS_ROOT_PATH}/{x}"
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"
        shutil.copy(scripts_path, notebooks_path)
        os.system(f"git add -f {notebooks_path}")


    ### Delete Unused ###

    for x in notebooks_remove_list:
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"
        os.remove(notebooks_path)