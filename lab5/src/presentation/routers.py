from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.common.event_bus import EventBus
from src.presentation.dependencies import get_db, get_event_bus
from src.presentation.schemas import UserRegisterSchema, ProductCreateSchema
from src.core import public as core_public
from src.analytics.application.queries import GetAnalyticsReportQuery, GetAnalyticsReportHandler

router = APIRouter()

@router.post("/users", status_code=201)
def register_user(schema: UserRegisterSchema, db: Session = Depends(get_db), event_bus: EventBus = Depends(get_event_bus)):
    try:
        user = core_public.register_user(
            db=db,
            event_bus=event_bus,
            username=schema.username,
            email=schema.email,
            role=schema.role
        )
        return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/products", status_code=201)
def create_product(schema: ProductCreateSchema, db: Session = Depends(get_db), event_bus: EventBus = Depends(get_event_bus)):
    try:
        product = core_public.create_product(
            db=db,
            event_bus=event_bus,
            title=schema.title,
            description=schema.description,
            price=schema.price,
            quantity=schema.quantity,
            farmer_id=schema.farmer_id
        )
        return {
            "id": product.id,
            "title": product.title,
            "price": product.price.value,
            "quantity": product.quantity.value,
            "farmer_id": product.farmer_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = core_public.get_all_products(db)
    return [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": p.price.value,
            "quantity": p.quantity.value,
            "farmer_id": p.farmer_id
        } for p in products
    ]

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    handler = GetAnalyticsReportHandler(db)
    query = GetAnalyticsReportQuery()
    return handler.execute(query)