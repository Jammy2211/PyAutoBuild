import glob
import datetime
import os
import re
import subprocess
import sys
import traceback

TIMEOUT_SECS = 36000
BUILD_PATH = os.getcwd()

BUILD_PYTHON_INTERPRETER = os.environ.get("BUILD_PYTHON_INTERPRETER", 'python3')
print(BUILD_PYTHON_INTERPRETER)


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
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        if e is subprocess.CalledProcessError:
            if "InversionException" in traceback.format_exc():
                return
            sys.exit()
            raise e
        # subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', f'{f}'], check=True)


def execute_script(f):
    args = [BUILD_PYTHON_INTERPRETER, f]
    print(f'Running <{args}>')
    try:
        subprocess.run(
            args,
            check=True,
            timeout=TIMEOUT_SECS,
        )
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:

        if "inversion" in f:
            return

        sys.exit()


def execute_scripts_in_folder(workspace_path, folder, root_path, scripts_no_run=None):

    scripts_no_run = scripts_no_run or []
    os.chdir(root_path)

    for script_dir in [t[0] for t in os.walk(".")]:
        scripts_path = f"{root_path}/{script_dir}"
        os.chdir(scripts_path)
        files = glob.glob(f"*.py")
        os.chdir(workspace_path)

        for f in files:
            run_script = True
            for no_run in scripts_no_run:
                if no_run in f:
                    run_script = False

            if run_script:
                execute_script(os.path.join('scripts', folder, script_dir, f))
