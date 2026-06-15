from src.domain.interfaces import UserRepository, ProductRepository
from src.domain.factory import DomainFactory
from src.domain.models import User, Product
from src.domain.exceptions import InvariantViolationError, DomainError

class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str, email: str, role: str) -> User:
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise InvariantViolationError("User with this email already exists")

        user = DomainFactory.create_user(
            id=None,
            username=username,
            email=email,
            role=role
        )

        return self.user_repo.save(user)


class AuthenticateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, email: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise DomainError("Invalid credentials")
        return user


class CreateProductUseCase:
    def __init__(self, product_repo: ProductRepository, user_repo: UserRepository):
        self.product_repo = product_repo
        self.user_repo = user_repo

    def execute(
        self,
        title: str,
        description: str,
        price_amount: float,
        quantity_value: int,
        farmer_id: int
    ) -> Product:
        farmer = self.user_repo.get_by_id(farmer_id)
        if not farmer:
            raise DomainError("Farmer profile not found")

        if farmer.role != "farmer":
            raise InvariantViolationError(
                "Only users with the 'farmer' role can create products"
            )

        product = DomainFactory.create_product(
            id=None,
            title=title,
            description=description,
            price_amount=price_amount,
            quantity_value=quantity_value,
            farmer_id=farmer_id
        )

        return self.product_repo.save(product)