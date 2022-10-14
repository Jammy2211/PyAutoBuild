import glob
import os
import shutil

import build_util

WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
PROJECTS_ROOT_PATH = f"{WORKSPACE_PATH}/projects"

PROJECTS_FOLDERS_OMIT = ["config", "dataset", "src"]


def generate_project_folders():
    os.chdir(PROJECTS_ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:

        ### PROJECTS FOLDER ###

        projects_path = f"{PROJECTS_ROOT_PATH}/{x}"

        if not sum([folder in projects_path for folder in PROJECTS_FOLDERS_OMIT]):

            ### Remove Old notebooks ###

            for f in glob.glob(f"{projects_path}/*.ipynb"):
                os.remove(f)
            for f in glob.glob(f"{projects_path}/*.ipynb_checkpoints"):
                shutil.rmtree(f)

            ### Convert ###

            os.chdir(projects_path)
            for f in glob.glob(f"*.py"):
                build_util.py_to_notebook(f)

            for f in glob.glob(f"*.ipynb"):
                build_util.uncomment_jupyter_magic(f)
                os.system(f"git add -f {projects_path}/{f}")

            if os.path.exists(f"{projects_path}/__init__.ipynb"):
                os.remove(f"{projects_path}/__init__.ipynb")

            if os.path.exists(f"{PROJECTS_ROOT_PATH}/__init__.ipynb"):
                os.remove(f"{PROJECTS_ROOT_PATH}/__init__.ipynb")

            for f in glob.glob(f"*.ipynb"):
                os.system(f"git add -f {projects_path}/{f}")
