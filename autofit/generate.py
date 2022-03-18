import os
import glob
import re
import shutil
import subprocess


import build_util


BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"
PROJECTS_ROOT_PATH = f"{WORKSPACE_PATH}/projects"
FOLDERS_OMIT = ["overview/simple", "overview/complex"]
COPY_VEBATIM_FILES = [
    "./features/analysis.py",
    "./features/model.py",
    "./searches/mcmc/analysis.py",
    "./searches/mcmc/model.py",
    "./searches/nest/analysis.py",
    "./searches/nest/model.py",
    "./searches/optimize/analysis.py",
    "./searches/optimize/model.py",
    "./howtofit/chapter_1_introduction/gaussian.py",
    "./howtofit/chapter_1_introduction/profiles.py",
    "./howtofit/chapter_database/profiles.py",
    "./howtofit/chapter_graphical_models/analysis.py",
    "./howtofit/chapter_graphical_models/gaussian.py",
    "./howtofit/chapter_graphical_models/profiles.py",
]
NOTEBOOKS_REMOVE = [
    "./features/analysis.ipynb",
    "./features/model.ipynb",
    "./searches/mcmc/analysis.ipynb",
    "./searches/mcmc/model.ipynb",
    "./searches/nest/analysis.ipynb",
    "./searches/nest/model.ipynb",
    "./searches/optimize/analysis.ipynb",
    "./searches/optimize/model.ipynb",
    "./howtofit/chapter_1_introduction/gaussian.ipynb",
    "./howtofit/chapter_1_introduction/profiles.ipynb",
    "./howtofit/chapter_database/profiles.ipynb",
    "./howtofit/chapter_graphical_models/analysis.ipynb",
    "./howtofit/chapter_graphical_models/gaussian.ipynb",
    "./howtofit/chapter_graphical_models/profiles.ipynb",
    "./overview/new_model_component/linear_fit.ipynb",
]

PROJECTS_FOLDERS_OMIT = ["config", "dataset", "src"]

def main():

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


    os.chdir(SCRIPTS_ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:

        scripts_path = f"{SCRIPTS_ROOT_PATH}/{x}"
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"

        if not sum([folder in notebooks_path for folder in FOLDERS_OMIT]):

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
                shutil.move(f"{scripts_path}/{f}", f"{notebooks_path}/{f}")
                os.system(f"git add -f {notebooks_path}/{f}")
            if os.path.exists(f"{notebooks_path}/__init__.ipynb"):
                os.remove(f"{notebooks_path}/__init__.ipynb")

            ### Copy README.rst files ###

            for f in glob.glob(f"*.rst"):
                shutil.copy(f"{scripts_path}/{f}", f"{notebooks_path}/{f}")
                os.system(f"git add -f {notebooks_path}/{f}")


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
