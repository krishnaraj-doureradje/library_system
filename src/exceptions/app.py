import logging

from fastapi.responses import JSONResponse

from src.models.error_response import ErrorResponse


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
    ):
        super().__init__()
        self.message = message
        self.status_code = status_code

    @property
    def logger(self) -> logging.Logger:
        """Returns the logger for the exception.

        Returns:
            logging.Logger: The logger for the exception.
        """
        return logging.getLogger("app")

    def log_exception(self) -> None:
        """Logs the exception."""
        self.logger.error(msg=self.message, exc_info=True, extra={"error": self.to_dict()})

    def to_dict(self) -> dict[str, str]:
        """Converts the exception to a dictionary.

        Returns:
            dict: The dictionary representation of the exception.
        """
        err_response = ErrorResponse(code=str(self.status_code), message=self.message)
        return err_response.model_dump()

    def to_json_response(self) -> JSONResponse:
        """Converts the exception to a JSONResponse.

        Returns:
            JSONResponse: The JSONResponse representation of the exception.
        """
        return JSONResponse(status_code=self.status_code, content=self.to_dict())


class SqlException(AppException):
    """SqlException base class"""

    pass


class NotFoundException(AppException):
    """NotFoundException base class"""

    pass


class BadRequestException(AppException):
    """BadRequestException base class"""

    pass


class AuthenticationException(AppException):
    """AuthenticationException base class"""

    pass
