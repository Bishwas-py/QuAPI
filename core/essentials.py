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

    def __str__(self):
        return f"<Essential.Request: {self.method}, {self.path}, {self.query}>"


class STATUS:
    OK_200 = "200 OK"
    CREATED_201 = "201 Created"
    ACCEPTED_202 = "202 Accepted"
    NO_CONTENT_204 = "204 No Content"
    MOVED_PERMANENTLY_301 = "301 Moved Permanently"
    FOUND_302 = "302 Found"
    SEE_OTHER_303 = "303 See Other"
    NOT_MODIFIED_304 = "304 Not Modified"
    TEMPORARY_REDIRECT_307 = "307 Temporary Redirect"
    PERMANENT_REDIRECT_308 = "308 Permanent Redirect"
    BAD_REQUEST_400 = "400 Bad Request"
    UNAUTHORIZED_401 = "401 Unauthorized"
    FORBIDDEN_403 = "403 Forbidden"
    NOT_FOUND_404 = "404 Not Found"
    METHOD_NOT_ALLOWED_405 = "405 Method Not Allowed"
    NOT_ACCEPTABLE_406 = "406 Not Acceptable"
    REQUEST_TIMEOUT_408 = "408 Request Timeout"
    CONFLICT_409 = "409 Conflict"
    GONE_410 = "410 Gone"
    LENGTH_REQUIRED_411 = "411 Length Required"
    PRECONDITION_FAILED_412 = "412 Precondition Failed"
    PAYLOAD_TOO_LARGE_413 = "413 Payload Too Large"
    URI_TOO_LONG_414 = "414 URI Too Long"   
    UNSUPPORTED_MEDIA_TYPE_415 = "415 Unsupported Media Type"
    RANGE_NOT_SATISFIABLE_416 = "416 Range Not Satisfiable"
    EXPECTATION_FAILED_417 = "417 Expectation Failed"
