from __future__ import annotations
from types import ModuleType
from typing import Any

import importlib
import logging

from core.initializers.router import paths
from core.constants import ENV, RESTRICTED_PATH_NAMES, GLOBAL_METHODS
from core.essentials import Request, RequestException, STATUS


def get_controller_name(request: Request) -> tuple:
    """
    This function returns the name of the controller file for a given request path or a 404 error
    message if the path is not found.

    :param request: The request object contains information about the incoming HTTP request, such as the
    request method, headers, and path. It is used to determine the appropriate controller to handle the
    request
    :type request: Request
    :return: a tuple containing the controller name for the given request path. If the path does not
    exist in the `paths` dictionary, it returns a 404 error message and status code. If the environment
    is set to production, it only returns the status code.
    """
    try:
        # This code is retrieving the name of the controller file that corresponds to the given
        # request path from the `paths` dictionary. The `paths` dictionary maps request paths to their
        # corresponding controller names. If the request path is not found in the `paths` dictionary,
        # it returns a 404 error message and status code. If the environment is set to production, it
        # only returns the status code.
        controller_name = paths[request.path]["controller_name"]
        return controller_name

    except KeyError:
        if ENV == "production":
            return "404 Not Found", "404 Not Found"
        return (
            f"404 Not Found [{request.path}]. Make sure you have a controller for this path"
            f" and you have resourced it to routes.yaml"
            "",
            "404 Not Found",
        )


def get_module(request: Request) -> ModuleType:
    """
    The function imports a module based on the name of a controller obtained from a request and raises
    an exception if the module is not found.

    :param request: The `request` parameter is an instance of the `Request` class, which is used to
    represent an HTTP request. It contains information about the request, such as the HTTP method,
    headers, and URL
    :type request: Request
    :return: a module object that corresponds to the controller name extracted from the request. If the
    module is not found, it raises a RequestException with a message and a 404 status code.
    """
    controller_name = get_controller_name(request)
    try:
        module = importlib.import_module(f"controllers.{controller_name}")
        return module
    except ModuleNotFoundError as exc:
        logging.error(f"Controller {controller_name} not found.")
        # return "Not Found.", "404 NOT FOUND"
        raise RequestException(
            f"Controller {controller_name} not found.",
            STATUS.NOT_FOUND_404,
        ) from exc


def execute_module_attr(module: ModuleType, request: Request, attr: str) -> Any:
    """
    This function executes a specified attribute of a given module and returns the result along with a
    status code.

    :param module: The `module` parameter is of type `ModuleType` and represents a Python module object.
    It is used to access the attributes (functions, variables, classes, etc.) defined in the module
    :type module: ModuleType
    :param request: The `request` parameter is an object that represents an HTTP request. It typically
    contains information such as the HTTP method (e.g. GET, POST), the URL being requested, any query
    parameters, headers, and the request body. This parameter is used in the function to pass along the
    request to
    :type request: Request
    :param attr: The `attr` parameter is a string representing the name of an attribute (function,
    variable, class, etc.) that we want to execute from a given module
    :type attr: str
    :return: The function `execute_module_attr` returns a tuple containing the result of calling the
    specified attribute (method or function) of the given module with the given request object, and a
    string "200 OK" indicating that the request was successful. If the specified attribute is not found
    in the module, a `RequestException` is raised with a 404 status code and an error message.
    """
    if hasattr(module, attr):
        controller_method = getattr(module, attr)
        return controller_method(request), "200 OK"

    error_message = f"404: {str(attr)} NOT FOUND"
    logging.error(error_message)
    raise RequestException(error_message, STATUS.NOT_FOUND_404)


def make_request(environ: dict) -> Request:
    """
    The function takes in a dictionary of environment variables and returns a validated request object.

    :param environ: The `environ` parameter is a dictionary containing the HTTP request information,
    such as the request method, headers, and query parameters. It is typically passed to a WSGI
    application by the web server
    :type environ: dict
    :return: a validated Request object.
    """
    request = Request(environ)
    return validate_request(request)


def format_path(path: str) -> str:
    """
    This function takes a request path as input and formats it according to the provided rules.
    :param path: The request path in a string format.
    :return: The formatted request path.
    """
    # If path is root or path already ends with index, return path after removing trailing slashes
    if path == "/" or path.endswith("/index"):
        return path.rstrip('/')

    split_path = path.split("/")

    # if path has more than 2 segments and the last segment is not empty, return path
    if len(split_path) > 2 and split_path[-1]:
        return path

    # For all other cases, append "/index" to the path and return
    return path.rstrip('/') + "/index"


def validate_request(request: Request) -> Request:
    """
    This function validates a request object and raises exceptions if the request method or path is not
    allowed.

    :param request: The `request` parameter is an instance of the `Request` class, which contains
    information about an HTTP request, such as the HTTP method, path, headers, and body
    :type request: Request
    :return: a validated Request object.
    """
    if not isinstance(request.method, str):
        raise RequestException("Method not understood", STATUS.METHOD_NOT_ALLOWED_405)

    if paths.get(request.path):
        if paths[request.path].get("allowed_methods") is not None:
            if request.method not in paths[request.path]["allowed_methods"]:
                raise RequestException(
                    f"Method is not allowed for path {request.path}",
                    STATUS.METHOD_NOT_ALLOWED_405,
                )
    else:
        request.path = format_path(request.path)

    if request.method not in GLOBAL_METHODS:
        raise RequestException(
            f"Method is not allowed for path {request.path}",
            STATUS.METHOD_NOT_ALLOWED_405,
        )

    return request
