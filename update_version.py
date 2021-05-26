import argparse
from datetime import date
import os
import re
import shutil
import subprocess


WORKSPACE = '../'
PROJECTS = [
        ('jonathanfrawley/PyAutoConf', 'autoconf'),
        ('jonathanfrawley/PyAutoFit', 'autofit'),
        ('jonathanfrawley/PyAutoArray', 'autoarray'),
        ('jonathanfrawley/PyAutoLens', 'autolens'),
        ('jonathanfrawley/PyAutoGalaxy', 'autogalaxy'),
        ]


def get_version_num(minor_version):
    today = date.today()
    today_str = today.strftime("%Y.%-m.%-d")
    return f'{today_str}.{minor_version}'


def update_version(repo_name, lib_name, version):
    old_dir = os.getcwd()
    os.chdir(f'{WORKSPACE}/{repo_name.split("/")[1]}')
    with open (f'{lib_name}/__init__.py', 'r' ) as f:
        file_content = f.read()
    file_content_with_version = re.sub(r'__version__\s*=\s*("|\')\d*\.\d*\.\d*(\.\d*)?("|\')', f'__version__ = "{version}"', file_content)
    with open (f'{lib_name}/__init__.py', 'w' ) as f:
        f.write(file_content_with_version)
    os.chdir(old_dir)


def update_all(mode, minor_version):
    old_dir = os.getcwd()
    version = get_version_num(minor_version)
    os.environ["VERSION"] = version

    for repo_name, lib_name in PROJECTS:
        try:
            print(f'Updating version of {repo_name}: {version}')
            update_version(repo_name, lib_name, version)
        except subprocess.CalledProcessError:
            raise Exception("Update failed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build all projects')
    parser.add_argument('--mode', type=str,
                        help='"test" or "prod"')

    parser.add_argument('--minor-version', type=int, default=1,
                        help='Minor version to use')

    args = parser.parse_args()
    os.makedirs(WORKSPACE, exist_ok=True)
    update_all(args.mode, int(args.minor_version))
