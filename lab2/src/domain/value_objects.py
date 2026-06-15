from dataclasses import dataclass
from .exceptions import InvalidValueError

@dataclass(frozen=True)
class Price:
    amount: float

    def __post_init__(self):
        if self.amount < 0:
            raise InvalidValueError("Price cannot be negative")

@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise InvalidValueError("Quantity cannot be negative")