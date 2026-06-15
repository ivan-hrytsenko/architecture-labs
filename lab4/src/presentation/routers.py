from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from src.presentation.schemas import UserRegisterSchema, ProductCreateSchema, ProductReadSchema
from src.presentation import dependencies
from src.domain.exceptions import InvariantViolationError
from src.application.commands.register_user import RegisterUserCommand
from src.application.commands.create_product import CreateProductCommand

router = APIRouter()

@router.post("/users", response_model=dict, status_code=201)
def register_user(
    schema: UserRegisterSchema,
    mode: str = Query("sync", pattern="^(sync|async)$"),
    fail_safely: bool = Query(False),
    handler_factory = Depends(dependencies.get_register_user_handler),
    notification_service = Depends(dependencies.get_notification_service)
):
    try:
        dependencies.get_notification_service(fail_safely)
        handler = handler_factory(mode=mode)
        command = RegisterUserCommand(
            username=schema.username,
            email=schema.email,
            role=schema.role
        )
        user_id = handler.handle(command)
        return {"id": user_id, "message": "User registered successfully"}
    except InvariantViolationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/products", response_model=dict, status_code=201)
def create_product(
    schema: ProductCreateSchema,
    mode: str = Query("sync", pattern="^(sync|async)$"),
    fail_safely: bool = Query(False),
    handler_factory = Depends(dependencies.get_create_product_handler),
    notification_service = Depends(dependencies.get_notification_service)
):
    try:
        dependencies.get_notification_service(fail_safely)
        handler = handler_factory(mode=mode)
        command = CreateProductCommand(
            title=schema.title,
            description=schema.description,
            price=schema.price,
            quantity=schema.quantity,
            farmer_id=schema.farmer_id
        )
        product_id = handler.handle(command)
        return {"id": product_id, "message": "Product created successfully"}
    except InvariantViolationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products", response_model=List[ProductReadSchema])
def get_products(handler = Depends(dependencies.get_all_products_handler)):
    return handler.handle()