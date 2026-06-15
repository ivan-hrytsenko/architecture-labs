from pydantic import BaseModel

class UserReadModel(BaseModel):
    id: int
    username: str
    email: str
    role: str

class ProductReadModel(BaseModel):
    id: int
    title: str
    description: str
    price: float
    quantity: int
    farmer_id: int