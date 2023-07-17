#!/usr/bin/env python3

import importlib
import json
import logging

from core.constants import ENV
from essentials import Request
from core.initializers.router import paths

GLOBAL_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
RESTRICTED_PATH_NAMES = ["/favicon.ico", "/robots.txt", "/sitemap.xml", "/"]


def render_api(environ):
    """
    Renders APIs, where actual path is unformulated slash containing string.
    :param environ: WSGI environment
    :return: tuple of (data, response)

    This function is the main handler for the server.
    It takes the WSGI environment and returns a tuple of (data, response).

    The data is the data that will be returned to the client.
    The response is the HTTP response code.

    The data can be a string, list, or dict.
    The response can be any valid HTTP response code.
    """
    request = Request(environ)
    if len(request.path.split("/")) == 2 and not request.path in RESTRICTED_PATH_NAMES:
        # if the path is a single slash, then it's a root path,
        # and we need to return the root controller; for /home it's home/index
        request.path = f"{request.path}/index"

    try:
        # now, we need to get the controller name
        # the controller name is the name of the controller file; for /home it's home/index.py
        # it doesn't use .get() because we want to raise an error if the path doesn't exist; aggressive
        controller_name = paths[request.path]['controller_name']
    except KeyError:
        if ENV == "production":
            return "404 Not Found", "404 Not Found"
        return f"404 Not Found [{request.path}]. Make sure you have a controller for this path" \
               f" and you have resourced it to routes.yaml""", "404 Not Found"

    if type(request.method) is not str:
        return "Request method is not understood.", "400 Bad Request"

    logging.info(f"[{request.method}] Request: {request.path}")

    try:
        if paths[request.path].get("allowed_methods") is not None:
            if request.method not in paths[request.path]["allowed_methods"]:
                return f"Method is not allowed for path {request.path}", "405 Method Not Allowed"

        mod = importlib.import_module(f"controllers.{controller_name}")
        if hasattr(mod, request.method.lower()):
            controller_method = getattr(mod, request.method.lower())
            return controller_method(request), "200 OK"
        elif request.method in GLOBAL_METHODS:
            logging.error(f"Method {request.method} not found in {controller_name}")
            return "Method not allowed.", "405 METHOD NOT ALLOWED"
        else:
            logging.error(f"The method {request.method} does not exist.")
            return f"The method {request.method} does not exist.", "405 METHOD NOT ALLOWED"

    except ModuleNotFoundError:
        logging.error(f"Controller {controller_name} not found.")
        return "Not Found.", "404 NOT FOUND"

    except KeyError as e:
        error_message = f"400: {str(e)} NOT FOUND"
        logging.error(error_message)
        return f"{error_message}", "400 NOT FOUND"

def destruct(dumped_data, response_status=None, dumped_data_content_type=None, access_control_allow_origin=None):
    if type(dumped_data) is list or type(dumped_data) is dict:
        dumped_data = json.dumps(dumped_data)
        dumped_data_content_type = "application/json" if dumped_data_content_type is None else dumped_data_content_type
    else:
        dumped_data = str(dumped_data)
        dumped_data_content_type = "text/plain"
    
    dumped_data_content_length = len(dumped_data)
    
    if not access_control_allow_origin:
        access_control_allow_origin = "*"
    logging.info(f'dumped_data_content_type: {dumped_data_content_type}')

    return dumped_data, response_status, dumped_data_content_type, access_control_allow_origin, dumped_data_content_length

# main server handler
def app(environ, start_response):
    response_tuple, response_status = render_api(environ)

    if type(response_tuple) is not tuple:
        response_tuple = (response_tuple,)

    (
        dumped_data, new_response_status, 
        dumped_data_content_type, access_control_allow_origin, 
        dumped_data_content_length
    ) = destruct(*response_tuple)


    response_status = new_response_status if new_response_status else response_status

    start_response(
        response_status, [
            ("Content-Type", dumped_data_content_type),
            ("Content-Length", str(dumped_data_content_length)),
            ("Access-Control-Allow-Origin", access_control_allow_origin)
        ]
    )
    return iter([dumped_data.encode("utf-8")])


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host_name',
                        type=str, help='Host name to run the server.', default='localhost')
    parser.add_argument('--port', dest='port_number',
                        type=int, help='Port number to run the server.', default=8000)
    args = parser.parse_args()
    
    httpd = make_server(args.host_name, args.port_number, app)
    logging.info(f"Serving on port {args.port_number}...")
    logging.info("Press Ctrl+C to stop.")
    logging.info(f'Visit http://{args.host_name}:{args.port_number}/')

    # Serve until process is killed
    httpd.serve_forever()
