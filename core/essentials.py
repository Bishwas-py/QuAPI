import json
from urllib.parse import parse_qs


class Request:
    accepts = {}

    method = ''
    body = ''
    path = ''

    query = {}
    params = {}

    cookies = {}
    files = {}

    server_name = ''
    server_port = ''
    user_agent = ''
    authorization = ''

    def __init__(self, environ):
        self.accepts = environ.get("HTTP_ACCEPT")
        self.method = environ.get("REQUEST_METHOD")
        self.path = environ.get("PATH_INFO")
        self.query = environ.get("QUERY_STRING")
        # self.params = environ.get("wsgiorg.routing_args")[1]
        self.server_name = environ.get("SERVER_NAME")
        self.server_port = environ.get("SERVER_PORT")
        self.user_agent = environ.get("HTTP_USER_AGENT")
        self.cookies = environ.get("HTTP_COOKIE")
        self.files = environ.get("wsgi.input")
        self.authorization = environ.get("HTTP_AUTHORIZATION")

        if self.method == 'POST':
            content_type = environ.get('CONTENT_TYPE', '').lower()
            if content_type == 'application/json':
                # Read and parse the request body as JSON
                content_length = int(environ.get('CONTENT_LENGTH', 0))
                if content_length > 0:
                    request_body = environ['wsgi.input'].read(content_length)
                    self.body = json.loads(request_body.decode('utf-8'))
                else:
                    self.body = {}
            elif content_type == 'application/x-www-form-urlencoded':
                # Read and parse the form data
                content_length = int(environ.get('CONTENT_LENGTH', 0))
                if content_length > 0:
                    request_body = environ['wsgi.input'].read(content_length)
                    self.body = parse_qs(request_body.decode('utf-8'))
                else:
                    self.body = {}
            else:
                self.body = {}
        else:
            self.body = {}


class Status:
    NOT_FOUND_404 = "404 Not Found"
    BAD_REQUEST_400 = "400 Bad Request"
    METHOD_NOT_ALLOWED_405 = "405 Method Not Allowed"
    OK_200 = "200 OK"
    FORBIDDEN_403 = "403 Forbidden"
