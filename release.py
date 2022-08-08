import argparse
import os
import re
import subprocess
from datetime import date

WORKSPACE = '../'
# MAX_MINOR_VERSION = 1
PROJECTS = [
    ('rhayes777/PyAutoConf', 'autoconf'),
    ('rhayes777/PyAutoFit', 'autofit'),
    ('Jammy2211/PyAutoArray', 'autoarray'),
    ('Jammy2211/PyAutoLens', 'autolens'),
    ('Jammy2211/PyAutoGalaxy', 'autogalaxy'),
]


def get_version_num(minor_version):
    today = date.today()
    today_str = today.strftime("%Y.%-m.%-d")
    return f'{today_str}.{minor_version}'


def update_version(repo_name, lib_name, version):
    old_dir = os.getcwd()
    os.chdir(f'{WORKSPACE}/{repo_name.split("/")[1]}')
    with open(f'{lib_name}/__init__.py', 'r') as f:
        file_content = f.read()
    file_content_with_version = re.sub(r'__version__\s*=\s*("|\')\d*\.\d*\.\d*(\.\d*)?("|\')',
                                       f'__version__ = "{version}"', file_content)

    with open(f'{lib_name}/__init__.py', 'w') as f:
        f.write(file_content_with_version)
    os.chdir(old_dir)


def build(repo_name):
    old_dir = os.getcwd()
    os.chdir(f'{WORKSPACE}/{repo_name.split("/")[1]}')
    subprocess.run(['python3', '-m', 'pip', 'install', '--upgrade', 'build'])
    subprocess.run(['python3', '-m', 'build'])
    os.chdir(old_dir)


def push_to_pypi(repo_name, mode):
    old_dir = os.getcwd()
    os.chdir(f'{WORKSPACE}/{repo_name.split("/")[1]}')
    if mode == 'test':
        subprocess.run(['python3', '-m', 'pip', 'install', '--user', '--upgrade', 'twine'])
        subprocess.check_output(['python3', '-m', 'twine', 'upload', '--repository', 'testpypi', 'dist/*'])
    elif mode == 'prod':
        subprocess.run(['python3', '-m', 'pip', 'install', '--user', '--upgrade', 'twine'])
        subprocess.check_output(['python3', '-m', 'twine', 'upload', 'dist/*'])
    else:
        raise ValueError('mode has to be one of "test", "prod"')
    os.chdir(old_dir)


def upload_all(mode, minor_version):
    old_dir = os.getcwd()
    version = get_version_num(minor_version)
    os.environ["VERSION"] = version

    for repo_name, lib_name in PROJECTS:
        try:
            print(f'Uploading version of {repo_name}: {version}')
            update_version(repo_name, lib_name, version)
            build(repo_name)
            push_to_pypi(repo_name, mode)
        except subprocess.CalledProcessError:
            print(
                f'Upload of {repo_name} with version {version} failed, retrying with minor_version {minor_version + 1}')
            raise Exception("Upload failed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build all projects')
    parser.add_argument('--mode', type=str,
                        help='"test" or "prod"')

    parser.add_argument('--minor-version', type=int, default=1,
                        help='Minor version to use')

    args = parser.parse_args()
    os.makedirs(WORKSPACE, exist_ok=True)
    upload_all(args.mode, int(args.minor_version))
