import importlib
import json
import os
import logging
import threading

from essentials import Request
from router import paths, CURRENT_DIR

GLOBAL_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
RESTRICTED_PATH_NAMES = ["/favicon.ico", "/robots.txt", "/sitemap.xml", "/"]

# stout logging
SERVER_LOG_FILE_PATH = os.path.join(CURRENT_DIR, "server.log")
# create file if it doesn't exist
if not os.path.exists(SERVER_LOG_FILE_PATH):
    open(SERVER_LOG_FILE_PATH, 'a').close()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(SERVER_LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)


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
        return f"""404 Not Found [{request.path}]. Make sure you have a controller
         for this path and you have resourced it to routes.yaml""", "404 Not Found"

    if type(request.method) is not str:
        return "Request method is not understood.", "400 Bad Request"

    logging.info(f"[{request.method}] Request: {request.path}")

    if request.path != "/":
        request.path = request.path.lstrip('/')

    try:
        mod = importlib.import_module(f"controllers.{controller_name}")
        if paths[request.path].get("allowed_methods") is not None:
            if request.method not in paths[request.path]["allowed_methods"]:
                return f"Method is not allowed for path {request.path}", "405 Method Not Allowed"
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


# main server handler
def app(environ, start_response):
    raw, response = render_api(environ)
    dumped_data = ''
    dumped_data_content_type = None
    access_control_allow_origin = '*'

    if type(raw) is tuple and len(raw) == 2:
        dumped_data = json.dumps(raw[0])
        dumped_data_content_type = raw[1]
    elif type(raw) is list:
        dumped_data = json.dumps(raw)
        dumped_data_content_type = 'application/json'
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
    task = threading.Thread(target=httpd.serve_forever)
    task.start()

