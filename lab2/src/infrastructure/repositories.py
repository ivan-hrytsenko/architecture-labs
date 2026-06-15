from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.interfaces import UserRepository, ProductRepository
from src.domain.models import User, Product
from .orm_models import UserORM, ProductORM
from .mappers import DataMapper

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        orm_user = self.session.query(UserORM).filter(UserORM.id == user_id).first()
        return DataMapper.user_to_domain(orm_user)

    def get_by_email(self, email: str) -> Optional[User]:
        orm_user = self.session.query(UserORM).filter(UserORM.email == email).first()
        return DataMapper.user_to_domain(orm_user)

    def save(self, user: User) -> User:
        orm_user = DataMapper.user_to_orm(user)
        if orm_user.id:
            self.session.merge(orm_user)
        else:
            self.session.add(orm_user)
        self.session.commit()
        self.session.refresh(orm_user)
        return DataMapper.user_to_domain(orm_user)

class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, product_id: int) -> Optional[Product]:
        orm_product = self.session.query(ProductORM).filter(ProductORM.id == product_id).first()
        return DataMapper.product_to_domain(orm_product)

    def get_all(self) -> List[Product]:
        orm_products = self.session.query(ProductORM).all()
        return [DataMapper.product_to_domain(p) for p in orm_products]

    def save(self, product: Product) -> Product:
        orm_product = DataMapper.product_to_orm(product)
        if orm_product.id:
            self.session.merge(orm_product)
        else:
            self.session.add(orm_product)
        self.session.commit()
        self.session.refresh(orm_product)
        return DataMapper.product_to_domain(orm_product)