from __future__ import annotations
from typing import Literal
from enum import Enum


import logging


class Request:
    accepts = {}

    method: str
    body: str
    path: str
    server_name: str
    server_port: str
    user_agent: str
    authorization: str

    query = {}
    params = {}

    cookies = {}
    files = {}

    def __init__(self, environ: dict) -> None:
        self.accepts = environ.get("HTTP_ACCEPT")
        self.method = str(environ.get("REQUEST_METHOD"))
        self.body = str(environ.get("wsgi.input"))
        self.path = str(environ.get("PATH_INFO"))
        self.query = str(environ.get("QUERY_STRING"))
        self.server_name = str(environ.get("SERVER_NAME"))
        self.server_port = str(environ.get("SERVER_PORT"))
        self.user_agent = str(environ.get("HTTP_USER_AGENT"))
        self.cookies = str(environ.get("HTTP_COOKIE"))
        self.files = str(environ.get("wsgi.input"))
        self.authorization = str(environ.get("HTTP_AUTHORIZATION"))

    def __str__(self):
        return f"<Essential.Request: {self.method}, {self.path}, {self.query}>"


class STATUS(Enum):
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
    UPGRADE_REQUIRED_426 = "426 Upgrade Required"
    PRECONDITION_REQUIRED_428 = "428 Precondition Required"
    TOO_MANY_REQUESTS_429 = "429 Too Many Requests"
    REQUEST_HEADER_FIELDS_TOO_LARGE_431 = "431 Request Header Fields Too Large"
    UNAVAILABLE_FOR_LEGAL_REASONS_451 = "451 Unavailable For Legal Reasons"
    INTERNAL_SERVER_ERROR_500 = "500 Internal Server Error"
    NOT_IMPLEMENTED_501 = "501 Not Implemented"
    BAD_GATEWAY_502 = "502 Bad Gateway"
    SERVICE_UNAVAILABLE_503 = "503 Service Unavailable"
    GATEWAY_TIMEOUT_504 = "504 Gateway Timeout"
    HTTP_VERSION_NOT_SUPPORTED_505 = "505 HTTP Version Not Supported"
    VARIANT_ALSO_NEGOTIATES_506 = "506 Variant Also Negotiates"
    INSUFFICIENT_STORAGE_507 = "507 Insufficient Storage"
    LOOP_DETECTED_508 = "508 Loop Detected"
    NOT_EXTENDED_510 = "510 Not Extended"
    NETWORK_AUTHENTICATION_REQUIRED_511 = "511 Network Authentication Required"


class RequestException(Exception):
    message: str
    status: Literal[
        STATUS.OK_200,
        STATUS.CREATED_201,
        STATUS.ACCEPTED_202,
        STATUS.NO_CONTENT_204,
        STATUS.MOVED_PERMANENTLY_301,
        STATUS.FOUND_302,
        STATUS.SEE_OTHER_303,
        STATUS.NOT_MODIFIED_304,
        STATUS.TEMPORARY_REDIRECT_307,
        STATUS.PERMANENT_REDIRECT_308,
        STATUS.BAD_REQUEST_400,
        STATUS.UNAUTHORIZED_401,
        STATUS.FORBIDDEN_403,
        STATUS.NOT_FOUND_404,
        STATUS.METHOD_NOT_ALLOWED_405,
        STATUS.NOT_ACCEPTABLE_406,
        STATUS.REQUEST_TIMEOUT_408,
        STATUS.CONFLICT_409,
        STATUS.GONE_410,
        STATUS.LENGTH_REQUIRED_411,
        STATUS.PRECONDITION_FAILED_412,
        STATUS.PAYLOAD_TOO_LARGE_413,
        STATUS.URI_TOO_LONG_414,
        STATUS.UNSUPPORTED_MEDIA_TYPE_415,
        STATUS.RANGE_NOT_SATISFIABLE_416,
        STATUS.EXPECTATION_FAILED_417,
        STATUS.UPGRADE_REQUIRED_426,
        STATUS.PRECONDITION_REQUIRED_428,
        STATUS.TOO_MANY_REQUESTS_429,
        STATUS.REQUEST_HEADER_FIELDS_TOO_LARGE_431,
        STATUS.UNAVAILABLE_FOR_LEGAL_REASONS_451,
        STATUS.INTERNAL_SERVER_ERROR_500,
        STATUS.NOT_IMPLEMENTED_501,
        STATUS.BAD_GATEWAY_502,
        STATUS.SERVICE_UNAVAILABLE_503,
        STATUS.GATEWAY_TIMEOUT_504,
        STATUS.HTTP_VERSION_NOT_SUPPORTED_505,
        STATUS.VARIANT_ALSO_NEGOTIATES_506,
        STATUS.INSUFFICIENT_STORAGE_507,
        STATUS.LOOP_DETECTED_508,
        STATUS.NOT_EXTENDED_510,
        STATUS.NETWORK_AUTHENTICATION_REQUIRED_511,
    ]

    def __init__(
        self,
        message: str,
        status: Literal[
            STATUS.OK_200,
            STATUS.CREATED_201,
            STATUS.ACCEPTED_202,
            STATUS.NO_CONTENT_204,
            STATUS.MOVED_PERMANENTLY_301,
            STATUS.FOUND_302,
            STATUS.SEE_OTHER_303,
            STATUS.NOT_MODIFIED_304,
            STATUS.TEMPORARY_REDIRECT_307,
            STATUS.PERMANENT_REDIRECT_308,
            STATUS.BAD_REQUEST_400,
            STATUS.UNAUTHORIZED_401,
            STATUS.FORBIDDEN_403,
            STATUS.NOT_FOUND_404,
            STATUS.METHOD_NOT_ALLOWED_405,
            STATUS.NOT_ACCEPTABLE_406,
            STATUS.REQUEST_TIMEOUT_408,
            STATUS.CONFLICT_409,
            STATUS.GONE_410,
            STATUS.LENGTH_REQUIRED_411,
            STATUS.PRECONDITION_FAILED_412,
            STATUS.PAYLOAD_TOO_LARGE_413,
            STATUS.URI_TOO_LONG_414,
            STATUS.UNSUPPORTED_MEDIA_TYPE_415,
            STATUS.RANGE_NOT_SATISFIABLE_416,
            STATUS.EXPECTATION_FAILED_417,
            STATUS.UPGRADE_REQUIRED_426,
            STATUS.PRECONDITION_REQUIRED_428,
            STATUS.TOO_MANY_REQUESTS_429,
            STATUS.REQUEST_HEADER_FIELDS_TOO_LARGE_431,
            STATUS.UNAVAILABLE_FOR_LEGAL_REASONS_451,
            STATUS.INTERNAL_SERVER_ERROR_500,
            STATUS.NOT_IMPLEMENTED_501,
            STATUS.BAD_GATEWAY_502,
            STATUS.SERVICE_UNAVAILABLE_503,
            STATUS.GATEWAY_TIMEOUT_504,
            STATUS.HTTP_VERSION_NOT_SUPPORTED_505,
            STATUS.VARIANT_ALSO_NEGOTIATES_506,
            STATUS.INSUFFICIENT_STORAGE_507,
            STATUS.LOOP_DETECTED_508,
            STATUS.NOT_EXTENDED_510,
            STATUS.NETWORK_AUTHENTICATION_REQUIRED_511,
        ],
    ) -> None:
        self.message = message
        self.status = status

    def http_error(self):
        logging.error(f"{self.message} - {self.status.value}")
        return f"{self.message}", self.status.value
