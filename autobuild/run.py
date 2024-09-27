import yaml
from pathlib import Path

import build_util

from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument("project", type=str, help="The project to build")
parser.add_argument("directory", type=str, help="The directory to build")
parser.add_argument(
    "--visualise",
    action="store_true",
    help="Only run notebooks for which we want to create visualisations",
)

args = parser.parse_args()

project = args.project
directory = args.directory
visualise = args.visualise

CONFIG_PATH = Path(__file__).parent / "config"

with open(CONFIG_PATH / "no_run.yaml") as f:
    no_run_dict = yaml.safe_load(f)

if visualise:
    with open(CONFIG_PATH / "visualise_notebooks.yaml") as f:
        visualise_list = yaml.safe_load(f)[project]
else:
    visualise_dict = None

if __name__ == "__main__":
    build_util.execute_notebooks_in_folder(
        no_run_list=no_run_dict[project],
        visualise_list=visualise_list,
        directory=directory,
    )
