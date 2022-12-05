# router.py is basically the router that handles all the requests and routes them to the correct controller.
# it configures the routes from routes.yaml and then it uses the controller name to import the controller and
# call the correct method (get, post, put, delete, etc.)

import os
import pathlib
import re
import yaml

from ..constants import CONTROLLERS_ROOT, LOG_COLOR


paths = {}

CURRENT_DIR = pathlib.Path(os.getcwd())

routes = yaml.load(open(CURRENT_DIR / "routes.yaml", "r"), Loader=yaml.FullLoader)

# sets the global root path domain.com/
if routes.get("root"):
    paths.update({
        '/': {'controller_name': routes.get("root")}
    })

resources = routes.get("resources")
tweaks = routes.get("tweaks")
controller_tweaks = tweaks.get("controller")
path_tweaks = tweaks.get("path")

for key, value in controller_tweaks.items():
    # Basically, reads and formats tweaks.controller from routes.yaml
    if type(value) is str:
        paths.update({
            f"/{value}": {'controller_name': key}
        })
    elif type(value) is dict:
        path = value.get("path")
        allowed_methods = value.get("allowed_methods")
        paths.update({
            f"{path}": {
                'controller_name': key,
                "allowed_methods": allowed_methods
            },
        })

for key, value in path_tweaks.items():
    # Reads and formats tweaks.path from routes.yaml
    # Basically, it's a way to add custom paths to the routes
    # without having to create a specific controller for it.
    paths.update({
        f"{key}": {'controller_name': value.get("controller")}
    })

if resources:
    for resource in resources:
        try:
            excluded_directories = {"__pycache__", "templates", "__init__.py"}
            controllers_dir = [x for x in os.listdir(os.path.join(CONTROLLERS_ROOT, resource)) if
                               x not in excluded_directories]

            for controller_file in controllers_dir:
                no_extension_controller_file_name = re.sub(r'\.py$', '', controller_file)
                controller_name = f"{resource}.{no_extension_controller_file_name}"
                path = f"/{resource}/{no_extension_controller_file_name}"
                paths.update(
                    {
                        path: {
                            'controller_name': controller_name
                        }
                    }
                )
        except FileNotFoundError as e:
            print(f"{LOG_COLOR.FAIL}FileNotFoundError: {e}{LOG_COLOR.ENDC}")
            print(
                f"{LOG_COLOR.WARNING}Please create a directory named '{resource}' in '{CONTROLLERS_ROOT}' directory.{LOG_COLOR.ENDC}")

# print paths as table
print(f"{LOG_COLOR.OK_CYAN}{'Path':<20}{'Controller':<20}{'Allowed Methods'}{LOG_COLOR.ENDC}")
for key, value in paths.items():
    print(f"{key:<20}{value.get('controller_name'):<20}{value.get('allowed_methods')}")
