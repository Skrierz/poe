# -*- coding: utf-8 -*-


class PoeExceptions(Exception):
    """Base exception class."""


class ServerAnswer(PoeExceptions):
    """Base exception for errors in server answer."""


class UnknownAnswer(ServerAnswer):
    """Unknown answer from server."""

    def __init__(self, server_answer):
        """Initialize exception."""
        self.message = server_answer

    def __str__(self):
        """Human readable representation."""
        return f'Unknown server answer: {self.message}'


class ForbiddenRequest(ServerAnswer):
    """Server return 'Forbidden'."""

    def __str__(self):
        """Human readable representation."""
        return 'Requested data is forbidden'


class ResourceNotFound(ServerAnswer):
    """Answer from server when character not found.

    Error example: {'error': {'code': 1, 'message': 'Resource not found'}}
    """

    def __str__(self):
        """Human readable representation."""
        return 'Character not found'


exceptions = {
    'Resource not found': ResourceNotFound,
    'Forbidden': ForbiddenRequest,
}


def server_error_router(server_error):
    """Router for server errors."""
    message = server_error.get('message')

    exception_class = exceptions.get(message)

    if exception_class is None:
        exception_class = UnknownAnswer(message)

    return exception_class
