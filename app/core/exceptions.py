from __future__ import annotations


class AppError(Exception):
    """Base app exception"""


class BadRequestError(AppError):
    pass


class NotFoundError(AppError):
    pass


class UnauthorizedError(AppError):
    pass


class ForbiddenError(AppError):
    pass


class ConflictError(AppError):
    pass


class TooManyRequestsError(AppError):
    pass