import datetime
import glob
import os
import re
import shutil
import subprocess


BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f'{os.getcwd()}/../autolens_workspace'
NOTEBOOKS_ROOT_PATH = f'{WORKSPACE_PATH}/notebooks'


def execute_notebook(f):
    print(f'Running <{f}> at {datetime.datetime.now().isoformat()}')
    subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--output', f, f], check=True)
    #subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', f'{f}'], check=True)


def main():
    os.chdir(NOTEBOOKS_ROOT_PATH)

    for x in [t[0] for t in os.walk('.')]:
        notebooks_path = f'{NOTEBOOKS_ROOT_PATH}/{x}'

        os.chdir(notebooks_path)
        for f in glob.glob(f'*.ipynb'):
            print(f'Processing <{x}/{f}>')
            execute_notebook(f)


if __name__ == '__main__':
    main()
