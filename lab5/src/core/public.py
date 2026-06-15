from sqlalchemy.orm import Session
from src.common.event_bus import EventBus
from src.core.application.commands.register_user import RegisterUserCommand, RegisterUserHandler
from src.core.application.commands.create_product import CreateProductCommand, CreateProductHandler
from src.core.application.queries.get_all_products import GetAllProductsQuery, GetAllProductsHandler
from src.core.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyProductRepository

def register_user(db: Session, event_bus: EventBus, username: str, email: str, role: str):
    repo = SQLAlchemyUserRepository(db)
    handler = RegisterUserHandler(repo, event_bus)
    command = RegisterUserCommand(username=username, email=email, role=role)
    return handler.execute(command)

def create_product(db: Session, event_bus: EventBus, title: str, description: str, price: float, quantity: int, farmer_id: int):
    user_repo = SQLAlchemyUserRepository(db)
    product_repo = SQLAlchemyProductRepository(db)
    handler = CreateProductHandler(user_repo, product_repo, event_bus)
    command = CreateProductCommand(title=title, description=description, price=price, quantity=quantity, farmer_id=farmer_id)
    return handler.execute(command)

def get_all_products(db: Session):
    handler = GetAllProductsHandler(db)
    query = GetAllProductsQuery()
    return handler.execute(query)