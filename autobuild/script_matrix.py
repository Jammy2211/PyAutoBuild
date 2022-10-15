#!/usr/bin/env python
import json
import os
import sys


def make_script_matrix(directory, project):
    _, directories, _ = list(os.walk(f"{project}/{directory}"))[0]
    directory_dicts = [
        {"project": project, "directory": directory}
        for directory in directories + ["."]
    ]
    return directory_dicts


def make_combined_script_matrix(directory, *projects):
    return [
        item for project in projects for item in make_script_matrix(directory, project)
    ]


if __name__ == "__main__":
    print(json.dumps(make_combined_script_matrix(*sys.argv[1:])))
