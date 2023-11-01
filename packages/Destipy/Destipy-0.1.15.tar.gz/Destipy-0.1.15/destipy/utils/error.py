import http

class InvalidStateException(Exception):
    """Invalid state error class for destipy."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'Invalid state error: {self.message}'

class DestipyException(Exception):
    """Base exception class for all exceptions raised by destipy.

    Args:
        message (str): The error message.
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class DestipyHTTPError(DestipyException):
    """HTTP Error

    Args:
        message (str): The error message.
        http_status (http.HTTPStatus): The HTTP status code.
    """
    def __init__(self, message: str, http_status: http.HTTPStatus):
        self.message = message
        self.http_status = http_status
        message = f'{message} (HTTP status code: {http_status})'
        super().__init__(message)


class RateLimitedError(Exception):
    """Rate limited error class for destipy."""
    def __init__(self, body, url, retry_after):
        self.body = body
        self.url = url
        self.retry_after = retry_after

    def __str__(self):
        return f'Rate limited error. Body: {self.body}, URL: {self.url}, Retry After: {self.retry_after}'

class DestipyRunTimeError(RuntimeError):
    """Runtime error class for destipy.
    """
