from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from decimal import Decimal

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = Field(..., pattern="^(farmer|customer)$")

class Token(BaseModel):
    access_token: str
    token_type: str

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    items: List[OrderItemSchema]