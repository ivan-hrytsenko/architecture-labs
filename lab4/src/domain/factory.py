import re
from typing import Optional
from .models import User, Product
from .value_objects import Price, Quantity
from .exceptions import InvalidValueError

class DomainFactory:
    @staticmethod
    def create_user(id: Optional[int], username: str, email: str, role: str) -> User:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise InvalidValueError("Invalid email format")
        if role not in ["farmer", "customer"]:
            raise InvalidValueError("Invalid system role")
        return User(id=id, username=username, email=email, role=role)

    @staticmethod
    def create_product(
        id: Optional[int], 
        title: str, 
        description: str, 
        price_amount: float, 
        quantity_value: int, 
        farmer_id: int
    ) -> Product:
        if not title.strip():
            raise InvalidValueError("Product title cannot be empty")
        return Product(
            id=id,
            title=title,
            description=description,
            price=Price(price_amount),
            quantity=Quantity(quantity_value),
            farmer_id=farmer_id
        )