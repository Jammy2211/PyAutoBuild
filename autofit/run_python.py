import os
import glob
import subprocess
import shutil


BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f"{os.getcwd()}/../autofit_workspace"
SCRIPTS_ROOT_PATH = f"{WORKSPACE_PATH}/scripts"


def run_python_script(f):
    args = ['python3', f]
    print(f'Running <{args}>')
    subprocess.run(args)


def main():
    os.chdir(SCRIPTS_ROOT_PATH)

    for x in [t[0] for t in os.walk(".")]:
        scripts_path = f"{SCRIPTS_ROOT_PATH}/{x}"
        if "__pycache__" in x:
            continue
        print(f"Processing dir <{x}>, {scripts_path}")

        os.chdir(scripts_path)
        for f in glob.glob(f"*.py"):
            run_python_script(f)

if __name__ == "__main__":
    main()
