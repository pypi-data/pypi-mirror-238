# -*- coding: utf-8 -*-


class APIException(Exception):
    """
    An exception related to usage of the Turon API.

    :param message: the error message to display.
    :param code: the HTTP status code associated with the HTTP response.
    """
    default_status_code = 500
    default_message = 'A server error occurred.'

    def __init__(self, message=None, code=None):
        self.message = message or self.default_message
        self.code = code or self.default_status_code


class Unauthorized(APIException):
    """
    Raised if an unauthorized request is made.
    """
    def __init__(self, message='Unauthorized request.', code=403):
        super().__init__(message=message, code=code)


class NotFound(APIException):
    """
    Raised if the requested resource is not found.
    """
    def __init__(self, message='Resource not found.', code=404):
        super().__init__(message=message, code=code)
