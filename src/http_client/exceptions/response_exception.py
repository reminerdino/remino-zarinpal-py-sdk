from typing import Optional


class ResponseException(Exception):
    def __init__(self, message: str, code: int, previous: Optional[Exception] = None,
                 error_details: Optional[dict] = None):
        super().__init__(message)
        self.code = code
        self.previous = previous
        self.error_details = error_details or {}

    def get_error_details(self) -> dict:
        return self.error_details

    def get_code(self) -> int:
        return self.code

    def get_previous(self) -> Optional[Exception]:
        return self.previous
