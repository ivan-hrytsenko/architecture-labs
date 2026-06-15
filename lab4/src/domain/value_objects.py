from dataclasses import dataclass
from src.domain.exceptions import InvariantViolationError

@dataclass(frozen=True)
class Price:
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise InvariantViolationError("Price cannot be negative")

@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise InvariantViolationError("Quantity cannot be negative")