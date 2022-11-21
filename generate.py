#!/bin/python3

import argparse
import logging
import os
import re

import pathlib

from rigids import SColor

currentPath = pathlib.Path(__file__).parent.resolve()


def generate_content(params, handler_name, content, extension):
    parent_name = params[0]
    child_name = params[1]

    file_path = f"{handler_name}/{parent_name}"
    directory = f"{currentPath / file_path}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    full_file_path = f"{directory}/{child_name}.{extension}"
    with open(full_file_path, "w") as f:
        f.write(content)
        logging.info(f"[CREATED] {file_path}/{child_name}.{extension}")


def controller_generator():
    content = """context = {
    'name': 'Job the wealthy'
}"""
    handler_name = 'controllers'
    extension = 'py'
    generate_content(args.controller, handler_name, content, extension)


# Instantiate the parser
parser = argparse.ArgumentParser(
    description=f'{SColor.OKCYAN}{SColor.BOLD}Generator Handler for {SColor.UNDERLINE}FyMO{SColor.ENDC}')

# make default value for controller
parser.add_argument('-c', '--controller', type=str,
                    help='The controller name that you wanna create with.', nargs=2)

args = parser.parse_args()

try:
    if args.controller:
        controller_generator()

except PermissionError:
    print(f"{SColor.FAIL}You don't have any permissions to do this, please use admin privileges.{SColor.ENDC}")
