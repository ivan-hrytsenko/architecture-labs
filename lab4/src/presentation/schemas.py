from pydantic import BaseModel

class UserRegisterSchema(BaseModel):
    username: str
    email: str
    role: str

class ProductCreateSchema(BaseModel):
    title: str
    description: str
    price: float
    quantity: int
    farmer_id: int

class ProductReadSchema(BaseModel):
    id: int
    title: str
    description: str
    price: float
    quantity: int
    farmer_id: int

    class Config:
        from_attributes = True