from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.database import SessionLocal
from src.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyProductRepository
from src.application.commands.register_user import RegisterUserHandler
from src.application.commands.create_product import CreateProductHandler
from src.application.queries.get_all_products import GetAllProductsHandler

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_repository(db: Session = Depends(get_db)):
    return SQLAlchemyUserRepository(db)

def get_product_repository(db: Session = Depends(get_db)):
    return SQLAlchemyProductRepository(db)

def get_register_user_handler(repo = Depends(get_user_repository)) -> RegisterUserHandler:
    return RegisterUserHandler(user_repo=repo)

def get_create_product_handler(
    product_repo = Depends(get_product_repository),
    user_repo = Depends(get_user_repository)
) -> CreateProductHandler:
    return CreateProductHandler(product_repo=product_repo, user_repo=user_repo)

def get_all_products_handler(db: Session = Depends(get_db)) -> GetAllProductsHandler:
    return GetAllProductsHandler(db_session=db)