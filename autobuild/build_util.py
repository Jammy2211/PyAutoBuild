import glob
import datetime
import logging
import os
import re
import subprocess
import sys
import traceback
from typing import List

TIMEOUT_SECS = 36000
BUILD_PATH = os.getcwd()

BUILD_PYTHON_INTERPRETER = os.environ.get("BUILD_PYTHON_INTERPRETER", "python3")
print(BUILD_PYTHON_INTERPRETER)


def py_to_notebook(filename):

    if filename == "temp.py":
        return

    subprocess.run(
        [
            "python3",
            f"{BUILD_PATH}/autobuild/add_notebook_quotes.py",
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


def no_run_list_with_extension_from(no_run_list: List[str], extension: str):

    for i, no_run in enumerate(no_run_list):
        if not no_run.endswith(extension):
            no_run_list[i] = f"{no_run}{extension}"

    return no_run_list


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

            logging.exception(e)

            if "InversionException" in traceback.format_exc():
                return
            sys.exit(1)
            raise e


def execute_notebooks_in_folder(ROOT_PATH, no_run_list=None):

    no_run_list = no_run_list or []

    no_run_list = no_run_list_with_extension_from(
        no_run_list=no_run_list, extension=".ipynb"
    )

    os.chdir(ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:

        notebooks_path = f"{ROOT_PATH}/{x}"
        os.chdir(notebooks_path)

        for f in glob.glob(f"*.ipynb"):
            if f not in no_run_list:
                execute_notebook(f)


def execute_script(f):

    args = [BUILD_PYTHON_INTERPRETER, f]
    print(f"Running <{args}>")

    try:
        subprocess.run(
            args, check=True, timeout=TIMEOUT_SECS,
        )
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:

        logging.exception(e)

        if "inversion" in f:
            return

        sys.exit(1)


def execute_scripts_in_folder(folder, no_run_list=None):

    no_run_list = no_run_list or []
    no_run_list = no_run_list_with_extension_from(
        no_run_list=no_run_list, extension=".py"
    )

    for script_dir in [t[0] for t in os.walk(".")]:
        os.chdir(folder)
        files = glob.glob(f"*.py")

        for f in sorted(files):
            if f not in no_run_list:
                execute_script(os.path.join("scripts", folder, script_dir, f))
