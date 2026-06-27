from fastapi import status


class AppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Internal Server Error"

    def __init__(self, message: str = None):
        if message:
            self.message = message


class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Not Found"


class UnprocessableEntityException(AppException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_CONTENT
    message = "Unprocessable Entity"
