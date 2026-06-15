from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.presentation.schemas import UserCreateSchema, ProductCreateSchema
from src.application.queries.read_models import ProductReadModel
from src.application.commands.register_user import RegisterUserCommand, RegisterUserHandler
from src.application.commands.create_product import CreateProductCommand, CreateProductHandler
from src.application.queries.get_all_products import GetAllProductsQuery, GetAllProductsHandler
from src.presentation.dependencies import (
    get_register_user_handler,
    get_create_product_handler,
    get_all_products_handler
)
from src.domain.exceptions import InvariantViolationError

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED)
def register_user(
    schema: UserCreateSchema,
    handler: RegisterUserHandler = Depends(get_register_user_handler)
):
    try:
        command = RegisterUserCommand(
            username=schema.username,
            email=schema.email,
            role=schema.role
        )
        user_id = handler.handle(command)
        return {"id": user_id}
    except InvariantViolationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    schema: ProductCreateSchema,
    handler: CreateProductHandler = Depends(get_create_product_handler)
):
    try:
        command = CreateProductCommand(
            title=schema.title,
            description=schema.description,
            price=schema.price,
            quantity=schema.quantity,
            farmer_id=schema.farmer_id
        )
        product_id = handler.handle(command)
        return {"id": product_id}
    except InvariantViolationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/products", response_model=List[ProductReadModel], status_code=status.HTTP_200_OK)
def get_products(handler: GetAllProductsHandler = Depends(get_all_products_handler)):
    query = GetAllProductsQuery()
    return handler.handle(query)