import os
import glob
import shutil


import build_util


BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autolens_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"
NOTEBOOKS_ROOT_PATH = f"{WORKSPACE_PATH}/notebooks"
COPY_VERBATIM_FOLDERS = []
COPY_VEBATIM_FILES = [
    "./imaging/preprocess/gui/scribbler.py",
    "./imaging/chaining/hyper_mode/extensions.py"
]
NOTEBOOKS_REMOVE = [
    "./imaging/preprocess/gui/scribbler.ipynb",
    "./imaging/chaining/hyper_mode/extensions.ipynb"
]


def main():
    os.chdir(SCRIPTS_ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:
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
