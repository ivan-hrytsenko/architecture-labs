from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from lab1.src.database import get_db, engine
from lab1.src.models.base import Base
from lab1.src.models.user import User
from lab1.src.schemas import UserCreate, Token, ProductCreate, OrderCreate
from lab1.src.auth import get_password_hash, verify_password, create_access_token, get_current_user
from lab1.src.services.product_service import ProductService
from lab1.src.services.order_service import OrderService, InsufficientStockError, OrderNotFoundError, InvalidOrderStatusError

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_pwd,
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email}

@app.post("/login", response_model=Token)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "farmer":
        raise HTTPException(status_code=403, detail="Only farmers can create products")
    return ProductService.create_listing(
        db, current_user.id, product_data.category_id,
        product_data.name, float(product_data.price), product_data.stock_quantity
    )

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def place_order(order_data: OrderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can place orders")
    try:
        items_dict = [item.dict() for item in order_data.items]
        return OrderService.place_order(db, current_user.id, items_dict)
    except InsufficientStockError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/orders/{order_id}/complete")
def complete_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return OrderService.complete_order(db, order_id)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidOrderStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return OrderService.cancel_order(db, order_id)
    except OrderNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidOrderStatusError as e:
        raise HTTPException(status_code=400, detail=str(e))