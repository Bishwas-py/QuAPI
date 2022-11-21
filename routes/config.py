import os
import re
from pathlib import Path

import yaml

from rigids import controllers_root, SColor

BASE_DIR = Path(__file__).resolve().parent.parent
CURRENT_DIR = Path(__file__).resolve().parent


def get_routes():
    with open(CURRENT_DIR / 'routes.yml', 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


routes = get_routes()

paths = {}
root_path = routes.get('root')
# sets the global root path domain.com/
if root_path:
    file_name = f"{root_path.replace('.', '/')}.svelte"
    paths.update({
        '/': {'template_path': file_name, 'controller_path': root_path}
    })

resources = routes.get('resources')
if resources:
    for resource in resources:
        try:
            templates_dir = os.listdir(BASE_DIR / f"{controllers_root}/{resource}")

            for controller_file in templates_dir:
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
