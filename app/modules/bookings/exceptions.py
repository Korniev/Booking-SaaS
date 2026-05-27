from app.core.exceptions import ConflictError, BadRequestError


class BookingOverlapError(ConflictError):
    pass


class InvalidBookingTimeError(BadRequestError):
    pass