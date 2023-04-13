#!/bin/python3

import argparse
import logging
import os
import pathlib

from constants import LOG_COLOR

CURRENT_PATH = pathlib.Path(os.getcwd())


def generate_content(params, handler_name, content, extension):
    parent_name = params[0]
    child_name = params[1]

    file_path = f"{handler_name}/{parent_name}"
    directory = f"{CURRENT_PATH / file_path}"

    if not os.path.exists(directory):
        os.makedirs(directory)

    full_file_path = f"{directory}/{child_name}.{extension}"
    with open(full_file_path, "w", encoding="UTF-8") as f:
        f.write(content)

        logging.info("[CREATED] {}/{}.{}".format(file_path, child_name, extension))


def controller_generator():
    """
    This function generates a Python controller file with a default "Hello World" response.
    """
    content = """def get(request):
    return "Hello World", "200 OK"
    """
    handler_name = "controllers"
    extension = "py"
    generate_content(args.controller, handler_name, content, extension)


# Instantiate the parser
parser = argparse.ArgumentParser(
    description="%fGenerator Handler for {LOG_COLOR.UNDERLINE}FyMO{LOG_COLOR.ENDC}"
    % LOG_COLOR.OK_CYAN
)

# make default value for controller
parser.add_argument(
    "-c",
    "--controller",
    type=str,
    help="The controller name that you wanna create with.",
    nargs=2,
)

args = parser.parse_args()

try:
    if args.controller:
        controller_generator()

except PermissionError:
    print(
        f"{LOG_COLOR.FAIL}You don't have any permissions to do this, please use admin privileges.{LOG_COLOR.ENDC}"
    )
