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


def main():

    os.chdir(SCRIPTS_ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:
        scripts_path = f"{SCRIPTS_ROOT_PATH}/{x}"
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"

        if not sum([folder in notebooks_path for folder in FOLDERS_OMIT]):

            if "__pycache__" in x:
                continue
            print(f"Processing dir <{x}>, {scripts_path} -> {notebooks_path}")

            # print("Removing old notebooks.")
            for f in glob.glob(f"{notebooks_path}/*.ipynb"):
                os.remove(f)
            for f in glob.glob(f"{notebooks_path}/*.ipynb_checkpoints"):
                shutil.rmtree(f)

            # print("Converting scripts to notebooks.")
            # print(scripts_path)
            os.chdir(scripts_path)
            # print(glob.glob(f'*.py'))
            for f in glob.glob(f"*.py"):
                build_util.py_to_notebook(f)
            # cd $WORKSPACE_PATH/generate

            # print(glob.glob(f'*.ipynb'))
            for f in glob.glob(f"*.ipynb"):
                # print(f'uncomment_jupyter_magic({f})')
                build_util.uncomment_jupyter_magic(f)

            # print("Copying Notebooks to notebooks folder.")
            # print(glob.glob(f'*.ipynb'))
            for f in glob.glob(f"*.ipynb"):
                if not os.path.exists(f"{notebooks_path}"):
                    print(f"Skipping {notebooks_path}/{f} as dest dir does not exist")
                    continue
                # print(f'{scripts_path}/{f} -> {notebooks_path}/{f}')
                shutil.move(f"{scripts_path}/{f}", f"{notebooks_path}/{f}")
                os.system(f"git add -f {notebooks_path}/{f}")
            if os.path.exists(f"{notebooks_path}/__init__.ipynb"):
                os.remove(f"{notebooks_path}/__init__.ipynb")

            # print("Running notebooks")
            """
            os.chdir(notebooks_path)
            for f in glob.glob(f'*.ipynb'):
                execute_notebook(f)
            """

    # Copy specific python files to notebooks folder
    for x in COPY_VEBATIM_FILES:
        scripts_path = f"{SCRIPTS_ROOT_PATH}/{x}"
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"
        shutil.copy(scripts_path, notebooks_path)
        os.system(f"git add -f {notebooks_path}")

    # Delete unused notebooks.
    for x in NOTEBOOKS_REMOVE:
        notebooks_path = f"{NOTEBOOKS_ROOT_PATH}/{x}"
        os.remove(notebooks_path)


if __name__ == "__main__":
    main()
