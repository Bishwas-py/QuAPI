#!/usr/bin/env python3

import logging
import json

from typing import Any

from core.essentials import RequestException

from core.utils import make_request
from core.utils import get_module
from core.utils import execute_module_attr


def render_api(environ: dict[str, str]) -> tuple:
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

    try:
        request = make_request(environ)
        logging.info(f"[{request.method}] Request: {request.path}")
        module = get_module(request)
        attr = request.method.lower()
        return execute_module_attr(module, request, attr)

    except RequestException as e:
        return e.http_error()


def destruct(
    dumped_data: Any,
    response_status=None,
    dumped_data_content_type=None,
    access_control_allow_origin=None,
) -> tuple:
    """
    The function takes in dumped data and other optional parameters, converts it to JSON or plain text,
    sets the content type and length, and returns a tuple of the data and other parameters.

    :param dumped_data: The data that has been dumped and needs to be returned in the response
    :type dumped_data: Any
    :param response_status: HTTP response status code (e.g. 200, 404, 500)
    :param dumped_data_content_type: The content type of the data that has been dumped. It can be either
    "application/json" or "text/plain"
    :param access_control_allow_origin: The `access_control_allow_origin` parameter is used to specify
    the domain(s) that are allowed to make cross-origin requests to the server. If this parameter is not
    provided, the default value of `*` (allowing all domains) is used
    :return: A tuple containing the following values:
    - dumped_data
    - response_status
    - dumped_data_content_type
    - access_control_allow_origin
    - dumped_data_content_length
    """
    if isinstance(dumped_data, (dict, list)):
        dumped_data = json.dumps(dumped_data)
        dumped_data_content_type = (
            "application/json"
            if dumped_data_content_type is None
            else dumped_data_content_type
        )
    else:
        dumped_data = str(dumped_data)
        dumped_data_content_type = "text/plain"

    dumped_data_content_length = len(dumped_data)

    if not access_control_allow_origin:
        access_control_allow_origin = "*"
    logging.info(f"dumped_data_content_type: {dumped_data_content_type}")

    return (
        dumped_data,
        response_status,
        dumped_data_content_type,
        access_control_allow_origin,
        dumped_data_content_length,
    )


def app(environ: dict, start_response: Any) -> Any:
    """
    The function takes in a dictionary and a function as input, renders an API response, destructures
    the response, sets the appropriate headers, and returns an encoded response.

    :param environ: A dictionary containing CGI-like environment variables, such as request method,
    headers, and query parameters
    :type environ: dict
    :param start_response: `start_response` is a callable function that is provided by the WSGI server.
    It takes two arguments: `status` and `response_headers`. `status` is a string that represents the
    HTTP status code and message, such as "200 OK" or "404 Not Found". `response
    :type start_response: Any
    :return: an iterator that contains a single element, which is the encoded version of the
    `dumped_data` variable.
    """
    response_tuple, response_status = render_api(environ)

    if not isinstance(response_tuple, tuple):
        response_tuple = (response_tuple,)
    (
        dumped_data,
        new_response_status,
        dumped_data_content_type,
        access_control_allow_origin,
        dumped_data_content_length,
    ) = destruct(*response_tuple)

    response_status = new_response_status if new_response_status else response_status

    start_response(
        response_status,
        [
            ("Content-Type", dumped_data_content_type),
            ("Content-Length", str(dumped_data_content_length)),
            ("Access-Control-Allow-Origin", access_control_allow_origin),
        ],
    )
    return iter([dumped_data.encode("utf-8")])


if __name__ == "__main__":
    # This code is setting up a command line interface for running the server on a specified host and
    # port number using the `argparse` module in Python. It defines two command line arguments
    # `--host` and `--port` which can be used to specify the host name and port number respectively.
    # The `args` object returned by `parser.parse_args()` is used to get the values of the command
    # line arguments. The `make_server` function from the `wsgiref.simple_server` module is used to
    # create a server instance with the specified host and port number, and the `app` function is
    # passed as the handler for the server. Finally, the server is started using the `serve_forever`
    # method of the server instance.
    from wsgiref.simple_server import make_server
    import argparse

    parser = argparse.ArgumentParser()

    # This code is defining a command line argument `--host` using the `argparse` module in Python.
    # The `--host` argument is used to specify the host name to run the server on.
    parser.add_argument(
        "--host",
        dest="host_name",
        type=str,
        help="Host name to run the server.",
        default="localhost",
    )

    # This code is defining a command line argument `--port` using the `argparse` module in Python.
    # The `--port` argument is used to specify the port number to run the server on. The `dest`
    # parameter specifies the name of the attribute to be added to the `args` object returned by
    # `parser.parse_args()`. The `type` parameter specifies the type of the argument, which in this
    # case is an integer. The `help` parameter provides a brief description of the argument. The
    # `default` parameter specifies the default value of the argument if it is not provided on the
    # command line.
    parser.add_argument(
        "--port",
        dest="port_number",
        type=int,
        help="Port number on which the server runs on",
        default=8000,
    )

    args = parser.parse_args()
    httpd = make_server(args.host_name, args.port_number, app)
    logging.info(f"Serving on port {args.port_number}...")
    logging.info("Press Ctrl+C to stop.")
    logging.info(f"Visit http://{args.host_name}:{args.port_number}/")

    # Serve until process is killed
    httpd.serve_forever(poll_interval=0.4)
