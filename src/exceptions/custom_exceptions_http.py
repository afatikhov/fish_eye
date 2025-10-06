from functools import wraps

from fastapi import HTTPException


class ICustomHttpException(BaseException):
    def to_http_exception(self) -> HTTPException:
        raise NotImplemented("Subclasses must implement this method!")

class NotFoundException(ICustomHttpException):
    def __init__(self, details: dict):
        super().__init__(details)
        self.details: dict = details

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=404,
                             detail=self.details)

class NotAddedException(ICustomHttpException):
    def __init__(self, details: dict):
        super().__init__(details)
        self.details: dict = details

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=400,
                             detail=self.details)

class NoUpdateWasMadeException(ICustomHttpException):
    def __init__(self, details: dict):
        super().__init__(details)
        self.details: dict = details

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=404,
                             detail=self.details)

class NoDataWasDeletedException(ICustomHttpException):
    def __init__(self, details: dict):
        super().__init__(details)
        self.details: dict = details

    def to_http_exception(self) -> HTTPException:
        return HTTPException(status_code=404,
                             detail=self.details)