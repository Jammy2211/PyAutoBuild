#!/usr/bin/env python
import json
import os
import sys


def make_script_matrix(parent_directory, project):
    try:
        _, directories, _ = list(os.walk(f"{project}/{parent_directory}"))[0]
        directory_dicts = [
            {
                "name": project,
                "directory": directory,
                "parent_directory": parent_directory,
            }
            for directory in directories + ["."]
        ]
        return directory_dicts
    except IndexError:
        return []


def make_combined_script_matrix(directory, projects):
    return [
        item for project in projects for item in make_script_matrix(directory, project)
    ]


if __name__ == "__main__":
    directories, *projects = sys.argv[1:]
    output = []
    for directory in directories.split(","):
        output += make_combined_script_matrix(directory, projects)
    print(json.dumps(output))
