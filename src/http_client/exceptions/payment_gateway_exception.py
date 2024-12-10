from typing import Optional


class ResponseException(Exception):
    def __init__(self, message: str, code: int, previous: Optional[Exception] = None):
        super().__init__(message)
        self.code = code
        self.previous = previous

    def get_code(self) -> int:
        return self.code

    def get_previous(self) -> Optional[Exception]:
        return self.previous


class PaymentGatewayException(ResponseException):
    def __init__(self, errors: dict):
        self.validation_errors = errors.get("validations", [])
        message = errors.get("message", "")
        code = errors.get("code", 0)
        super().__init__(message, code)

    def get_validation_errors(self) -> list:
        return self.validation_errors
