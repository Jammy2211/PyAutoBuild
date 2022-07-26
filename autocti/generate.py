import os
import glob
import shutil


import build_util


BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autocti_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"
PROJECTS_ROOT_PATH = f"{WORKSPACE_PATH}/projects"
COPY_VERBATIM_FOLDERS = []
COPY_VEBATIM_FILES = []
NOTEBOOKS_REMOVE = []


def main():

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
            os.makedirs(notebooks_path, exist_ok=True)
            shutil.move(f"{scripts_path}/{f}", f"{notebooks_path}/{f}")
            os.system(f"git add -f {notebooks_path}/{f}")

        if os.path.exists(f"{notebooks_path}/__init__.ipynb"):
            os.remove(f"{notebooks_path}/__init__.ipynb")


        ### Copy README.rst files ###

        for f in glob.glob(f"*.rst"):
            shutil.copy(f"{scripts_path}/{f}", f"{notebooks_path}/{f}")
            os.system(f"git add -f {notebooks_path}/{f}")


    ### Copy specific Folders ###

    for x in COPY_VERBATIM_FOLDERS:
        scripts_path = f"{SCRIPTS_ROOT_PATH}/{x}"
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"
        if "__pycache__" in x:
            continue
        print(f"Processing dir <{x}>, {scripts_path} -> {notebooks_path}")

        # print("Removing old notebooks.")
        for f in glob.glob(f"{notebooks_path}/*.ipynb"):
            os.remove(f)
        for f in glob.glob(f"{notebooks_path}/*.ipynb_checkpoints"):
            shutil.rmtree(f)

        os.chdir(scripts_path)
        for f in glob.glob(f"*.py"):
            shutil.copy(f"{scripts_path}/{f}", f"{notebooks_path}/{f}")
            os.system(f"git add -f {notebooks_path}/{f}")
        if os.path.exists(f"{notebooks_path}/__init__.ipynb"):
            os.remove(f"{notebooks_path}/__init__.ipynb")


    ### Copy specific Python Files ###

    for x in COPY_VEBATIM_FILES:
        scripts_path = f"{SCRIPTS_ROOT_PATH}/{x}"
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"
        shutil.copy(scripts_path, notebooks_path)
        os.system(f"git add -f {notebooks_path}")


    ### Delete Unused ###

    for x in NOTEBOOKS_REMOVE:
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"
        os.remove(notebooks_path)


if __name__ == "__main__":
    main()
