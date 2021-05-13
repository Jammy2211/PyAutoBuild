import glob
import datetime
import os
import re
import subprocess

TIMEOUT_SECS = 60
BUILD_PATH = os.getcwd()


def py_to_notebook(filename):
    if filename == "temp.py":
        return
    # print(f'py_to_notebook: {filename}')
    subprocess.run(
        [
            "python3",
            f"{BUILD_PATH}/add_notebook_quotes/add_notebook_quotes.py",
            filename,
            "temp.py",
        ],
        check=True,
    )
    subprocess.run(
        ["ipynb-py-convert", "temp.py", f'{filename.split(".py")[0]}.ipynb'], check=True
    )
    os.remove("temp.py")


def uncomment_jupyter_magic(f):
    with open(f, "r") as sources:
        lines = sources.readlines()
    with open(f, "w") as sources:
        for line in lines:
            line = re.sub(r"# %matplotlib", "%matplotlib", line)
            line = re.sub(r"# from pyproj", "from pyproj", line)
            line = re.sub(r"# workspace_path", "workspace_path", line)
            line = re.sub(r"# %cd", "%cd", line)
            line = re.sub(r"# print\(f", "print(f", line)
            sources.write(line)


def exexcute_notebooks_in_folder(ROOT_PATH, NOTEBOOKS_NO_RUN=None):

    NOTEBOOKS_NO_RUN = NOTEBOOKS_NO_RUN or []

    os.chdir(ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:

        notebooks_path = f"{ROOT_PATH}/{x}"
        os.chdir(notebooks_path)

        for f in glob.glob(f"*.ipynb"):

            run_notebook = True
            for no_run in NOTEBOOKS_NO_RUN:
                if no_run in f:
                    run_notebook = False

            if run_notebook:
                execute_notebook(f)


def execute_notebook(f):
    print(f"Running <{f}> at {datetime.datetime.now().isoformat()}")
    try:
        subprocess.run(
            ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--output", f, f],
            check=True,
            timeout=TIMEOUT_SECS,
        )
    except subprocess.TimeoutExpired as e:
        print(f"Timed out executing <{f}>")
        # subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', f'{f}'], check=True)


def execute_python_script(f):
    args = ['python3', f]
    print(f'Running <{args}>')
    subprocess.run(args, check=True)


def execute_python_scripts(workspace_path):
    build_path = os.getcwd()
    scripts_root_path = f"{workspace_path}/scripts"

    os.chdir(scripts_root_path)
    script_dirs = [t[0] for t in os.walk(".")]
    os.chdir(workspace_path)
    for script_dir in script_dirs:
        scripts_path = f"scripts/{script_dir}"
        if "__pycache__" in script_dir:
            continue
        print(f"Processing dir <{script_dir}>, {scripts_path}")

        os.chdir(scripts_path)
        files = glob.glob(f"*.py")
        os.chdir(workspace_path)  # Scripts need to be run from here
        for f in files:
            execute_python_script(os.path.join(scripts_path, f))
