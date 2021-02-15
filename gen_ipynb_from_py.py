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
    #print(f'py_to_notebook: {filename}')
    subprocess.run(['python3', f'{BUILD_PATH}/add_notebook_quotes/add_notebook_quotes.py', filename, 'temp.py'], check=True)
    subprocess.run(["ipynb-py-convert", 'temp.py', f'{filename.split(".py")[0]}.ipynb'], check=True)
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



BUILD_PATH = os.getcwd()
WORKSPACE_PATH = f'{os.getcwd()}/../autolens_workspace'
SCRIPTS_ROOT_PATH = f'{WORKSPACE_PATH}/scripts'
NOTEBOOKS_ROOT_PATH = f'{WORKSPACE_PATH}/notebooks'
COPY_VERBATIM_FOLDERS = ['./howtolens/chapter_3_pipelines/pipelines']


def main():
    os.chdir(SCRIPTS_ROOT_PATH)

    for x in [t[0] for t in os.walk('.')]:
        scripts_path = f'{SCRIPTS_ROOT_PATH}/{x}'
        notebooks_path = f'{NOTEBOOKS_ROOT_PATH}/{x}'
        if '__pycache__' in x:
            continue
        print(f'Processing dir <{x}>, {scripts_path} -> {notebooks_path}')

        #print("Removing old notebooks.")
        for f in glob.glob(f'{notebooks_path}/*.ipynb'):
            os.remove(f)
        for f in glob.glob(f'{notebooks_path}/*.ipynb_checkpoints'):
            shutil.rmtree(f)

        #print("Converting scripts to notebooks.")
        #print(scripts_path)
        os.chdir(scripts_path)
        #print(glob.glob(f'*.py'))
        for f in glob.glob(f'*.py'):
            py_to_notebook(f)
        #cd $WORKSPACE_PATH/generate

        #print(glob.glob(f'*.ipynb'))
        for f in glob.glob(f'*.ipynb'):
            #print(f'uncomment_jupyter_magic({f})')
            uncomment_jupyter_magic(f)

        #print("Copying Notebooks to notebooks folder.")
        #print(glob.glob(f'*.ipynb'))
        for f in glob.glob(f'*.ipynb'):
            if not os.path.exists(f'{notebooks_path}'):
                print(f'Skipping {notebooks_path}/{f} as dest dir does not exist')
                continue
            #print(f'{scripts_path}/{f} -> {notebooks_path}/{f}')
            shutil.move(f'{scripts_path}/{f}', f'{notebooks_path}/{f}')
        if os.path.exists(f'{notebooks_path}/__init__.ipynb'):
            os.remove(f'{notebooks_path}/__init__.ipynb')

        #print("Running notebooks")
        '''
        os.chdir(notebooks_path)
        for f in glob.glob(f'*.ipynb'):
            execute_notebook(f)
        '''

    for x in COPY_VERBATIM_FOLDERS:
        scripts_path = f'{SCRIPTS_ROOT_PATH}/{x}'
        notebooks_path = f'{NOTEBOOKS_ROOT_PATH}/{x}'
        if '__pycache__' in x:
            continue
        print(f'Processing dir <{x}>, {scripts_path} -> {notebooks_path}')

        #print("Removing old notebooks.")
        for f in glob.glob(f'{notebooks_path}/*.ipynb'):
            os.remove(f)
        for f in glob.glob(f'{notebooks_path}/*.ipynb_checkpoints'):
            shutil.rmtree(f)

        os.chdir(scripts_path)
        for f in glob.glob(f'*.py'):
            shutil.copy(f'{scripts_path}/{f}', f'{notebooks_path}/{f}')
        if os.path.exists(f'{notebooks_path}/__init__.ipynb'):
            os.remove(f'{notebooks_path}/__init__.ipynb')

        #print("Running notebooks")
        '''
        os.chdir(notebooks_path)
        for f in glob.glob(f'*.ipynb'):
            execute_notebook(f)
        '''


if __name__ == '__main__':
    main()
