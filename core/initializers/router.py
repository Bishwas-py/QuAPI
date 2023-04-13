# This code is responsible for parsing a `routes.yaml` file and generating a dictionary of paths and
# their corresponding controllers and allowed methods. It first opens the `routes.yaml` file and loads
# its contents into a Python dictionary using the `yaml.load()` method. It then iterates through the
# dictionary and adds paths to the `paths` dictionary based on the values of certain keys. It also
# checks for custom paths and controllers specified in the `tweaks` dictionary and adds them to the
# `paths` dictionary. Finally, it prints out a table of the paths and their corresponding controllers
# and allowed methods.

import os
import pathlib
import re
import yaml

from ..constants import CONTROLLERS_ROOT, LOG_COLOR

paths = {}

CURRENT_DIR = pathlib.Path(os.getcwd())

# This code block is opening the `routes.yaml` file located in the current directory (`CURRENT_DIR`)
# in read mode with UTF-8 encoding. It then loads the contents of the file into a Python dictionary
# using the `yaml.load()` method with the `yaml.FullLoader` loader. The resulting dictionary is stored
# in the `routes` variable.
with open(CURRENT_DIR / "routes.yaml", "r", encoding="UTF-8") as route_yaml_file:
    routes = yaml.load(route_yaml_file, Loader=yaml.FullLoader)

# sets the global root path domain.com/
if routes.get("root"):
    paths.update({"/": {"controller_name": routes.get("root")}})

resources = routes.get("resources")
tweaks = routes.get("tweaks")
controller_tweaks = tweaks.get("controller")
path_tweaks = tweaks.get("path")

# This code block is iterating through the items in the `controller_tweaks` dictionary. For each
# key-value pair, it checks if the type of the value is a string. If it is, it adds a new path to the
# `paths` dictionary with the key `f"/{value}"` and the value `{"controller_name": key}`. This is used
# to create a custom path for a controller without having to specify a path in the `routes.yaml` file.
for key, value in controller_tweaks.items():
    # This code block checks if the type of `value` is a string. If it is, it adds a new path to the
    # `paths` dictionary with the key `f"/{value}"` and the value `{"controller_name": key}`. This is
    # used to create a custom path for a controller without having to specify a path in the
    # `routes.yaml` file.
    if isinstance(type(value), str):
        paths.update({f"/{value}": {"controller_name": key}})

    # This code block is checking if the type of `value` is a dictionary. If it is, it extracts the
    # `path` and `allowed_methods` values from the dictionary and adds a new path to the `paths`
    # dictionary with the extracted values. This is used to create a custom path for a controller with
    # specific allowed methods without having to specify a path in the `routes.yaml` file.
    elif isinstance(type(value), dict):
        path = value.get("path")
        allowed_methods = value.get("allowed_methods")
        paths.update(
            {
                f"{path}": {"controller_name": key, "allowed_methods": allowed_methods},
            }
        )

for key, value in path_tweaks.items():
    # Reads and formats tweaks.path from routes.yaml
    # Basically, it's a way to add custom paths to the routes
    # without having to create a specific controller for it.
    paths.update({f"{key}": {"controller_name": value.get("controller")}})

if resources:
    for resource in resources:
        try:
            # check if the controller exists
            excluded_directories = {"__pycache__", "templates", "__init__.py"}
            controllers_dir = [
                x
                for x in os.listdir(os.path.join(CONTROLLERS_ROOT, resource))
                if x not in excluded_directories
            ]

            for controller_file in controllers_dir:
                no_extension_controller_file_name = re.sub(
                    r"\.py$", "", controller_file
                )
                controller_name = f"{resource}.{no_extension_controller_file_name}"

                # check if controller_name is in tweaks.controller, and unique path is set, if so, don't add it
                if controller_name in controller_tweaks:
                    if controller_tweaks.get(controller_name).get("unique"):
                        continue

                path = f"/{resource}/{no_extension_controller_file_name}"
                paths.update({path: {"controller_name": controller_name}})
        except FileNotFoundError as e:
            print(f"{LOG_COLOR.FAIL}FileNotFoundError: {e}{LOG_COLOR.ENDC}")
            print(
                f"{LOG_COLOR.WARNING}Please create a directory named '{resource}' in '{CONTROLLERS_ROOT}' directory.{LOG_COLOR.ENDC}"
            )

# This code block is printing out a table of the paths and their corresponding controllers and allowed
# methods. It first prints out a header row with the column names "Path", "Controller", and "Allowed
# Methods" in the specified color. Then, for each key-value pair in the `paths` dictionary, it prints
# out a row with the path, controller name, and allowed methods (if any) in a formatted table. The
# `<20` in the f-strings is used to left-align the text within each column and ensure that each column
# is 20 characters wide.

print(
    f"{LOG_COLOR.OK_CYAN}{'Path':<20}{'Controller':<20}{'Allowed Methods'}{LOG_COLOR.ENDC}"
)
for key, value in paths.items():
    print(f"{key:<20}{value.get('controller_name'):<20}{value.get('allowed_methods')}")
