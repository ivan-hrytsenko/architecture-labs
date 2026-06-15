from dataclasses import dataclass
from src.domain.interfaces import UserRepository, ProductRepository
from src.domain.factory import DomainFactory
from src.domain.exceptions import InvariantViolationError
from src.application.commands.base import CommandHandler

@dataclass(frozen=True)
class CreateProductCommand:
    title: str
    description: str
    price: float
    quantity: int
    farmer_id: int

class CreateProductHandler(CommandHandler[CreateProductCommand, int]):
    def __init__(self, product_repo: ProductRepository, user_repo: UserRepository):
        self._product_repo = product_repo
        self._user_repo = user_repo

    def handle(self, command: CreateProductCommand) -> int:
        farmer = self._user_repo.get_by_id(command.farmer_id)
        if not farmer:
            raise InvariantViolationError("Farmer not found")
        
        if farmer.role != "farmer":
            raise InvariantViolationError("Only users with the 'farmer' role can create products")

        product = DomainFactory.create_product(
            id=None,
            title=command.title,
            description=command.description,
            price=command.price,
            quantity=command.quantity,
            farmer_id=command.farmer_id
        )
        saved_product = self._product_repo.save(product)
        return saved_product.id