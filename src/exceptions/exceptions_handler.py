from functools import wraps

from exceptions.custom_exceptions_http import ICustomHttpException


def http_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ICustomHttpException as e:
            raise e.to_http_exception()
    return wrapper