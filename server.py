import importlib
import json
import re
from pathlib import Path
import logging

from essentials import Request
from routes.config import paths

BASE_DIR = Path(__file__).resolve().parent

# stout logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def render_api(environ):
    """
    Renders APIs, where actual path is unformulated slash containing string.
    """
    request = Request(environ)

    controller_name = paths[request.path]['controller_name']

    if type(request.method) is not str:
        return "Request method is not understood.", "400 Bad Request"

    logging.info(f"[{request.method}] Request: {request.path}")

    if request.path != "/":
        request.path = request.path.lstrip('/')

    #  paths[path] gives filename i.e. index.svelte
    try:
        mod = importlib.import_module(f"controllers.{controller_name}")
        if hasattr(mod, request.method.lower()):
            controller_method = getattr(mod, request.method.lower())
            logging.info(f"Controller method: {controller_method}")
            return controller_method(request), "200 OK"
        else:
            logging.error(f"Method {request.method} not found in {controller_name}")
            return "Method not allowed.", "405 METHOD NOT ALLOWED"
    except ModuleNotFoundError:
        return "Not Found.", "404 NOT FOUND"
    except KeyError as e:
        error_message = f"400: {str(e)} NOT FOUND"
        logging.error(error_message)
        return f"{error_message}", "400 NOT FOUND"


# main server handler
def app(environ, start_response):
    raw, response = render_api(environ)
    dumped_data = ''
    dumped_data_content_type = None
    access_control_allow_origin = '*'

    if type(raw) is tuple and len(raw) == 2:
        dumped_data = json.dumps(raw[0])
        dumped_data_content_type = raw[1]
    elif type(raw) is str:
        dumped_data = raw
        dumped_data_content_type = "text/plain"
    elif type(raw) is dict:
        dumped_data = json.dumps(raw)
        dumped_data_content_type = "application/json"

    dumped_data_content_length = len(dumped_data)

    start_response(
        response, [
            ("Content-Type", dumped_data_content_type),
            ("Content-Length", str(dumped_data_content_length)),
            ("Access-Control-Allow-Origin", access_control_allow_origin)
        ]
    )
    return iter([dumped_data.encode("utf-8")])


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    httpd = make_server("localhost", 8000, app)
    logging.info("Serving on port 8000...")
    logging.info("Press Ctrl+C to stop.")
    logging.info('Visit http://localhost:8000/')
    httpd.serve_forever()
