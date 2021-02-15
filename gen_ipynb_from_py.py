import os
import glob
import re
import shutil
import subprocess

#function notebook_to_py {
#    find . -name "*.ipynb" -exec bash -c 'ipynb-py-convert "$1" temp.py ; cat temp.py | sed "s/# %%//g" > "${1/\.ipynb/.py}"' _ {} \;
#    rm temp.py
#}
#function py_to_notebook {
#    find . -name "*.py" -exec bash -c 'add_notebook_quotes.py "$1" temp.py ; ipynb-py-convert temp.py "${1/\.py/.ipynb}"' _ {} \;
#    rm temp.py
#}

def py_to_notebook(filename):
    if filename == 'temp.py':
        return
    print(f'py_to_notebook: {filename}')
    subprocess.run(['python3', f'{BUILD_PATH}/add_notebook_quotes/add_notebook_quotes.py', filename, 'temp.py'])
    subprocess.run(["ipynb-py-convert", 'temp.py', f'{filename.split(".py")[0]}.ipynb'])
    os.remove('temp.py')

def uncomment_jupyter_magic(f):
    with open(f, "r") as sources:
        lines = sources.readlines()
    with open(f, "w") as sources:
        for line in lines:
            line = re.sub(r'# %matplotlib', '%matplotlib', line)
            line = re.sub(r'# from pyproj', 'from pyproj', line)
            line = re.sub(r'# workspace_path', 'workspace_path', line)
            line = re.sub(r'# %cd', '%cd', line)
            line = re.sub(r'# print\(f', 'print(f', line)
            sources.write(line)

def execute_notebook(f):
    #subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--output', f'"{f}"', f'"{f}"'])
    subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', f'{f}'])


print("Setting up Environment variables.")
BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f'{os.getcwd()}/../autolens_workspace'

SCRIPTS_PATH = f'{WORKSPACE_PATH}/scripts/database'

NOTEBOOKS_PATH = f'{WORKSPACE_PATH}/notebooks/database'

print("Removing old notebooks.")
for f in glob.glob(f'{NOTEBOOKS_PATH}/*.ipynb'):
    os.remove(f)
for f in glob.glob(f'{NOTEBOOKS_PATH}/*.ipynb_checkpoints'):
    shutil.rmtree(f)

print("Converting scripts to notebooks.")
print(SCRIPTS_PATH)
os.chdir(SCRIPTS_PATH)
print(glob.glob(f'*.py'))
for f in glob.glob(f'*.py'):
    py_to_notebook(f)
#cd $WORKSPACE_PATH/generate

print(glob.glob(f'*.ipynb'))
for f in glob.glob(f'*.ipynb'):
    print(f'uncomment_jupyter_magic({f})')
    uncomment_jupyter_magic(f)

print("Copying Notebooks to notebooks folder.")
print(glob.glob(f'*.ipynb'))
for f in glob.glob(f'*.ipynb'):
    print(f'{f} -> {NOTEBOOKS_PATH}/{f}')
    shutil.move(f, f'{NOTEBOOKS_PATH}/{f}')
os.remove(f'{NOTEBOOKS_PATH}/__init__.ipynb')

print("Running notebooks")
os.chdir(NOTEBOOKS_PATH)
for f in glob.glob(f'*.ipynb'):
    execute_notebook(f)

#echo "Renaming notebook methods"
#find $NOTEBOOKS_PATH/*.ipynb -type f -exec sed -i 's/# %matplotlib/%matplotlib/g' {} +
#find $NOTEBOOKS_PATH/*.ipynb -type f -exec sed -i 's/# from pyproj/from pyproj/g' {} +
#find $NOTEBOOKS_PATH/*.ipynb -type f -exec sed -i 's/# workspace_path/workspace_path/g' {} +
#find $NOTEBOOKS_PATH/*.ipynb -type f -exec sed -i 's/# %cd/%cd/g' {} +
#find $NOTEBOOKS_PATH/*.ipynb -type f -exec sed -i 's/# print(f/print(f/g' {} +
#
# TODO Next, convert these.
#echo "Running notebooks."
#cd $NOTEBOOKS_PATH
#for f in $NOTEBOOKS_PATH/*.ipynb; do jupyter nbconvert --to notebook --execute --output ""$f"" "$f"; done
#cd $WORKSPACE_PATH/generate
