from datetime import date
import os
import re
import shutil
import subprocess


WORKSPACE = 'build_workspace'
MAX_MINOR_VERSION = 100
PROJECTS = [('Jammy2211/PyAutoArray', 'autoarray')]


def get_version_num(minor_version):
    today = date.today()
    today_str = today.strftime("%Y%m%d")
    return f'{today_str}.{minor_version}'


def clone_repo(repo_name):
    old_dir = os.getcwd()
    os.chdir(WORKSPACE)
    subprocess.run(['git', 'clone', f'https://github.com/{repo_name}'])
    os.chdir(old_dir)


def update_version(repo_name, lib_name, version):
    old_dir = os.getcwd()
    os.chdir(f'{WORKSPACE}/{repo_name.split("/")[1]}')
    with open (f'{lib_name}/__init__.py', 'r' ) as f:
        file_content = f.read()
    file_content_with_version = re.sub(r'__version__\s*=\s*"\d*\.\d*\.\d*"', f'__version__ = "{version}"', file_content)
    with open (f'{lib_name}/__init__.py', 'w' ) as f:
        f.write(file_content_with_version)
    os.chdir(old_dir)


def build(repo_name):
    old_dir = os.getcwd()
    os.chdir(f'{WORKSPACE}/{repo_name.split("/")[1]}')
    #. ~/miniconda3/bin/activate
    #conda activate PyAutoLens
    subprocess.run(['python3', '-m', 'pip', 'install', '--upgrade', 'build'])
    subprocess.run(['python3', '-m', 'build'])
    os.chdir(old_dir)


def push_to_pypi(repo_name):
    old_dir = os.getcwd()
    os.chdir(f'{WORKSPACE}/{repo_name.split("/")[1]}')
    subprocess.run(['python3', '-m', 'pip', 'install', '--user', '--upgrade', 'twine'])
    subprocess.check_output(['python3', '-m', 'twine', 'upload', '--repository', 'testpypi', 'dist/*'])
    os.chdir(old_dir)


def upload_all(minor_version):
    old_dir = os.getcwd()
    for repo_name, lib_name in PROJECTS:
        try:
            version = get_version_num(minor_version)
            print(f'Uploading version of {repo_name}: {version}')
            os.environ["VERSION"] = version
            clone_repo(repo_name)
            update_version(repo_name, lib_name, version)
            build(repo_name)
            push_to_pypi(repo_name)
            #push_to_git()
        except subprocess.CalledProcessError:
            print(f'Upload with minor version {minor_version} failed, retrying with minor_version {minor_version+1}')
            os.chdir(old_dir)
            shutil.rmtree(f'{WORKSPACE}/{repo_name.split("/")[1]}')
            upload_all(minor_version + 1)
            return

if __name__ == '__main__':
    upload_all(1)
