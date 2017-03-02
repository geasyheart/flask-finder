from functools import wraps

from flask import jsonify


class ServiceException(Exception):
    error_code = 0
    message = ""

    def __init__(self, error_code=None, message=None):
        if error_code and error_code != 0:
            self.error_code = error_code
        if message:
            self.message = message

    def to_dict(self):
        return {
            "error_code": self.error_code,
            "message": self.message
        }


class FieldNameError(ServiceException):
    error_code = 100
    message = "field name error!"


class FieldEqualError(ServiceException):
    error_code = 101
    message = "requests error!"


class ArgsError(ServiceException):
    error_code = 102
    message = "args error!"


class ServiceTypeError(ServiceException):
    error_code = 103
    message = "type error!"


def api_view(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            if resp is None:
                resp = {"message": ""}
            if isinstance(resp, bytes):
                resp = resp.decode()
            if not isinstance(resp, dict):
                resp = {"message": resp}
            resp.setdefault("error_code", 0)
        except ServiceException as e:
            resp = e.to_dict()
        except TypeError:
            resp = ServiceTypeError().to_dict()
        return jsonify(**resp)

    return wrapper
