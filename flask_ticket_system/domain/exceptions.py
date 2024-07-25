from kytool.domain.exceptions import InternalException


class AssigmentException(InternalException):
    pass


class InvalidCredentialsException(InternalException):
    pass


class TicketNotFoundException(InternalException):
    pass


class UnauthorizedException(InternalException):
    pass
