import os
import re
from pathlib import Path

from rigids import controllers_root, SColor
from routes.routes import Routes

BASE_DIR = Path(__file__).resolve().parent.parent
CURRENT_DIR = Path(__file__).resolve().parent

routes = Routes()

paths = {}

# sets the global root path domain.com/
if routes.root:
    paths.update({
        '/': {'controller_path': routes.root}
    })

if routes.tweaked_routes:
    for key, value in routes.tweaked_routes.items():
        print(key, value)
        if type(value) is dict:
            paths.update({
                value['path']: {'controller_path': key}
            })
        else:
            paths.update({
                value: {'controller_path': key}
            })

if routes.resources:
    for resource in routes.resources:
        try:
            controllers_dir = os.listdir(BASE_DIR / f"{controllers_root}/{resource}")

            for controller_file in controllers_dir:
                no_extension_controller_file_name = re.sub(r'\.py$', '', controller_file)
                controller_path = f"{resource}.{no_extension_controller_file_name}"
                paths.update(
                    {
                        f"{resource}/{no_extension_controller_file_name}": {
                            'controller_path': controller_path
                        }
                    }
                )
        except FileNotFoundError as e:
            print(f"{SColor.FAIL}FileNotFoundError: {e}{SColor.ENDC}")
            print(
                f"{SColor.WARNING}Please create a directory named '{resource}' in '{controllers_root}' directory.{SColor.ENDC}")
