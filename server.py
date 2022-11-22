import importlib
import json
from pathlib import Path
import logging

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
    path = environ.get("PATH_INFO")
    controller_name = paths[path]['controller_path']

    request_headers = environ.get("HTTP_ACCEPT")
    request_method = environ.get("REQUEST_METHOD")
    request_body = ''

    if type(request_method) is not str:
        return "Request method is not understood.", "400 Bad Request"

    request = {
        "path": path,
        "headers": request_headers,
        "method": request_method,
        "body": request_body
    }

    logging.info(f"Request: {request}")

    if path != "/":
        path = path.lstrip('/')

    #  paths[path] gives filename i.e. index.svelte
    try:
        mod = importlib.import_module(f"controllers.{controller_name}")
        controller_method = getattr(mod, request_method.lower())
        return controller_method(request), "200 OK"

    except KeyError as e:
        error_message = f"400: {str(e)} not found"
        logging.error(error_message)
        return f"{error_message}", "400 NOT FOUND"


# main server handler
def app(environ, start_response):
    raw, response = render_api(environ)
    dumped_data = json.dumps(raw)
    start_response(
        response, [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(dumped_data)))
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
