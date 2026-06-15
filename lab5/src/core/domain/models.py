import re
from typing import Optional
from src.core.domain.value_objects import Price, Quantity
from src.core.domain.exceptions import InvalidValueError

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    role: str

@dataclass
class Product:
    id: Optional[int]
    title: str
    description: str
    price: Price
    quantity: Quantity
    farmer_id: int

    def update_stock(self, new_quantity: int):
        self.quantity = Quantity(new_quantity)

    def reduce_stock(self, amount: int):
        if amount > self.quantity.value:
            raise InvariantViolationError("Not enough stock available")
        self.quantity = Quantity(self.quantity.value - amount)