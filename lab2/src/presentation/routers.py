from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from sqlalchemy.orm import Session

from src.infrastructure.database import SessionLocal
from src.infrastructure.repositories import SQLAlchemyUserRepository, SQLAlchemyProductRepository
from src.application.use_cases import RegisterUserUseCase, AuthenticateUserUseCase, CreateProductUseCase
from src.domain.exceptions import DomainError
from .dtos import UserRegisterDTO, UserLoginDTO, TokenDTO, ProductCreateDTO, ProductResponseDTO

router = APIRouter()

SECRET_KEY = "super-secret-key-for-lab-2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(dto: UserRegisterDTO, db: Session = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(db)
    use_case = RegisterUserUseCase(user_repo)
    try:
        user = use_case.execute(dto.username, dto.email, dto.role)
        return {"id": user.id, "username": user.username, "email": user.email, "role": user.role}
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenDTO)
def login(dto: UserLoginDTO, db: Session = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(db)
    use_case = AuthenticateUserUseCase(user_repo)
    try:
        user = use_case.execute(dto.email)
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/products", response_model=ProductResponseDTO, status_code=status.HTTP_201_CREATED)
def create_product(
    dto: ProductCreateDTO, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    user_repo = SQLAlchemyUserRepository(db)
    product_repo = SQLAlchemyProductRepository(db)
    use_case = CreateProductUseCase(product_repo, user_repo)
    try:
        product = use_case.execute(dto.title, dto.description, dto.price, dto.quantity, current_user_id)
        return ProductResponseDTO(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price.amount,
            quantity=product.quantity.value,
            farmer_id=product.farmer_id
        )
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/products", response_model=list[ProductResponseDTO])
def get_products(db: Session = Depends(get_db)):
    product_repo = SQLAlchemyProductRepository(db)
    products = product_repo.get_all()
    return [
        ProductResponseDTO(
            id=p.id,
            title=p.title,
            description=p.description,
            price=p.price.amount,
            quantity=p.quantity.value,
            farmer_id=p.farmer_id
        ) for p in products
    ]