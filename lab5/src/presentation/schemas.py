from pydantic import BaseModel, EmailStr

class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    role: str

class ProductCreateSchema(BaseModel):
    title: str
    description: str
    price: float
    quantity: int
    farmer_id: int