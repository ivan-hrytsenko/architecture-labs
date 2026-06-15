class DomainError(Exception):
    pass

class InvalidValueError(DomainError):
    pass

class InvariantViolationError(DomainError):
    pass