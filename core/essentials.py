import json


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
        self.body = environ.get("wsgi.input")
        self.path = environ.get("PATH_INFO")
        self.query = environ.get("QUERY_STRING")
        # self.params = environ.get("wsgiorg.routing_args")[1]
        self.server_name = environ.get("SERVER_NAME")
        self.server_port = environ.get("SERVER_PORT")
        self.user_agent = environ.get("HTTP_USER_AGENT")
        self.cookies = environ.get("HTTP_COOKIE")
        self.files = environ.get("wsgi.input")
        self.authorization = environ.get("HTTP_AUTHORIZATION")
