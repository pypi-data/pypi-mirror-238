import enum


class CheckStatusCode(enum.Enum):
    FAILED = 0
    OK = 1
    CREATED = 2
    NO_CONTENT = 3


class HTTPStatusCode(enum.Enum):
    INTERNAL_SERVER_ERROR = 500
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
