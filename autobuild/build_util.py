import datetime
import logging
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path
from typing import List

TIMEOUT_SECS = 36000
BUILD_PATH = Path(__file__).parent

BUILD_PYTHON_INTERPRETER = os.environ.get("BUILD_PYTHON_INTERPRETER", "python3")
print(BUILD_PYTHON_INTERPRETER)


def py_to_notebook(filename: Path):
    subprocess.run(
        ["python3", f"{BUILD_PATH}/add_notebook_quotes.py", filename, "temp.py"],
        check=True,
    )
    new_filename = filename.with_suffix(".ipynb")
    subprocess.run(
        ["ipynb-py-convert", "temp.py", new_filename], check=True,
    )
    os.remove("temp.py")
    uncomment_jupyter_magic(new_filename)
    return new_filename


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


def execute_notebooks_in_folder(directory, no_run_list):
    files = Path.cwd().rglob(f"{directory}/*.ipynb")

    for file in sorted(files):
        if file.stem not in no_run_list:
            execute_notebook(file)


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


def execute_scripts_in_folder(directory, no_run_list=None):
    no_run_list = no_run_list or []

    files = Path.cwd().rglob(f"{directory}/*.py")

    for file in sorted(files):
        if file.stem not in no_run_list:
            execute_script(str(file))
