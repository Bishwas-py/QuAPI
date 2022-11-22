import os
import re
from pathlib import Path

from rigids import controllers_root, SColor
# import PyYAML
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CURRENT_DIR = Path(__file__).resolve().parent

paths = {}

env = os.environ.get("ENV", "development")

routes = yaml.load(open(os.path.join(CURRENT_DIR, "routes.yaml"), "r"), Loader=yaml.FullLoader)

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
    if type(value) is str:
        paths.update({
            f"/{value}": {'controller_name': key}
        })
    elif type(value) is dict:
        path = value.get("path")
        allowed_methods = value.get("allowed_methods")
        paths.update({
            f"{path}": {'controller_name': key},
            "allowed_methods": allowed_methods
        })

for key, value in path_tweaks.items():
    paths.update({
        f"{key}": {'controller_name': value}
    })

if resources:
    for resource in resources:
        try:
            excluded_directories = {"__pycache__", "templates", "__init__.py"}
            controllers_dir = [x for x in os.listdir(os.path.join(controllers_root, resource)) if
                               x not in excluded_directories]

            for controller_file in controllers_dir:
                no_extension_controller_file_name = re.sub(r'\.py$', '', controller_file)
                controller_name = f"{resource}.{no_extension_controller_file_name}"
                path = f"{resource}/{no_extension_controller_file_name}"
                paths.update(
                    {
                        path: {
                            'controller_name': controller_name
                        }
                    }
                )
        except FileNotFoundError as e:
            print(f"{SColor.FAIL}FileNotFoundError: {e}{SColor.ENDC}")
            print(
                f"{SColor.WARNING}Please create a directory named '{resource}' in '{controllers_root}' directory.{SColor.ENDC}")
