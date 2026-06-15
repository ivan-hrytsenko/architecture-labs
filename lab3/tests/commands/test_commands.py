import pytest
from src.domain.models import User, Product
from src.domain.interfaces import UserRepository, ProductRepository
from src.domain.exceptions import InvariantViolationError
from src.application.commands.register_user import RegisterUserCommand, RegisterUserHandler
from src.application.commands.create_product import CreateProductCommand, CreateProductHandler

class FakeUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self._counter = 1

    def get_by_id(self, user_id: int) -> User:
        return self.users.get(user_id)

    def get_by_email(self, email: str) -> User:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def save(self, user: User) -> User:
        if user.id is None:
            user.id = self._counter
            self._counter += 1
        self.users[user.id] = user
        return user

class FakeProductRepository(ProductRepository):
    def __init__(self):
        self.products = {}
        self._counter = 1

    def get_by_id(self, product_id: int) -> Product:
        return self.products.get(product_id)

    def get_all(self) -> list[Product]:
        return list(self.products.values())

    def save(self, product: Product) -> Product:
        if product.id is None:
            product.id = self._counter
            self._counter += 1
        self.products[product.id] = product
        return product


def test_register_user_command_success():
    user_repo = FakeUserRepository()
    handler = RegisterUserHandler(user_repo=user_repo)
    command = RegisterUserCommand(username="ivan_h", email="ivan@example.com", role="farmer")

    user_id = handler.handle(command)

    assert user_id == 1
    assert user_repo.get_by_id(1).username == "ivan_h"


def test_register_user_command_duplicate_email_throws_error():
    user_repo = FakeUserRepository()
    handler = RegisterUserHandler(user_repo=user_repo)
    command = RegisterUserCommand(username="ivan_h", email="ivan@example.com", role="farmer")
    handler.handle(command)

    with pytest.raises(InvariantViolationError):
        handler.handle(command)


def test_create_product_by_non_farmer_throws_error():
    user_repo = FakeUserRepository()
    product_repo = FakeProductRepository()
    
    user = User(id=1, username="buyer_ivan", email="buyer@example.com", role="buyer")
    user_repo.save(user)

    handler = CreateProductHandler(product_repo=product_repo, user_repo=user_repo)
    command = CreateProductCommand(
        title="Молоко",
        description="Свіже молоко",
        price=45.0,
        quantity=10,
        farmer_id=1
    )

    with pytest.raises(InvariantViolationError):
        handler.handle(command)