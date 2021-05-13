import argparse
import os
import subprocess

#WORKSPACE = '../'
WORKSPACE = './workspace_tmp'

LIB_PROJECTS = [
    'PyAutoConf', 'PyAutoFit', 'PyAutoArray', 'PyAutoLens', 'PyAutoGalaxy'
    ]

WORKSPACE_PROJECTS = [
    'autolens_workspace', 'autolens_test_workspace'
    ]

def main(version):
    for project in LIB_PROJECTS:
        print(f'Tagging {project}')
        old_dir = os.getcwd()
        os.chdir(os.path.join(WORKSPACE, project))
        subprocess.run(['git', 'commit', '-a', '-m', 'Update version to {version}'], check=True)
        subprocess.run(['git', 'tag', f'v{version}'], check=True)
        #subprocess.run(['git', 'push', 'origin', 'master', '--tags'], check=True)
        os.chdir(old_dir)

    for project in WORKSPACE_PROJECTS:
        print(f'Tagging {project}')
        old_dir = os.getcwd()
        os.chdir(os.path.join(WORKSPACE, project))
        subprocess.run(['git', 'commit', '-a', '-m', f'Update version to {version}'], check=True)
        subprocess.run(['git', 'tag', f'v{version}'], check=True)
        #subprocess.run(['git', 'push', 'origin', 'master', '--tags'], check=True)
        subprocess.run(['git', 'fetch'], check=True)
        subprocess.run(['git', 'checkout', 'release'], check=True)
        subprocess.run(['git', 'merge', 'master'], check=True)
        #subprocess.run(['git', 'push', 'origin', 'release'], check=True)
        os.chdir(old_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tag and merge projects for release')
    parser.add_argument('--version', type=str, required=True,
                        help='Version to use')

    args = parser.parse_args()
    main(args.version)
