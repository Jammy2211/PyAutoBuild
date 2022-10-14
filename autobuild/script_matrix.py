#!/usr/bin/env python

import json
import os
import sys


def make_script_matrix(project, directory):
    _, directories, _ = list(os.walk(directory))[0]
    directory_dicts = [
        {"project": project, "directory": directory}
        for directory in directories + ["."]
    ]
    return json.dumps(directory_dicts)


if __name__ == "__main__":
    print(make_script_matrix(*sys.argv[1:]))
