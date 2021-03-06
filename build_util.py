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