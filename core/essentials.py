class Request:
    headers = {}
    method = ''
    body = ''
    path = ''
    query = {}
    params = {}
    cookies = {}
    files = {}

    def __init__(self, environ):
        self.headers = environ.get("HTTP_ACCEPT")
        self.method = environ.get("REQUEST_METHOD")
        self.body = environ.get("wsgi.input")
        self.path = environ.get("PATH_INFO")
        self.query = environ.get("QUERY_STRING")
        # self.params = environ.get("wsgiorg.routing_args")[1]
        self.cookies = environ.get("HTTP_COOKIE")
        self.files = environ.get("wsgi.input")
