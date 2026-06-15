from pydantic import BaseModel, EmailStr

class UserRegisterDTO(BaseModel):
    username: str
    email: EmailStr
    role: str

class UserLoginDTO(BaseModel):
    email: str

class TokenDTO(BaseModel):
    access_token: str
    token_type: str

class ProductCreateDTO(BaseModel):
    title: str
    description: str
    price: float
    quantity: int

class ProductResponseDTO(BaseModel):
    id: int
    title: str
    description: str
    price: float
    quantity: int
    farmer_id: int

    class Config:
        from_attributes = True