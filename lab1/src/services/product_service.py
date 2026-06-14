from sqlalchemy.orm import Session
from lab1.src.repositories.product_repository import ProductRepository
from lab1.src.models.product import Category

class ProductService:
    @staticmethod
    def get_or_create_category(db: Session, name: str, description: str = None):
        cat = db.query(Category).filter(Category.name == name).first()
        if not cat:
            cat = Category(name=name, description=description)
            db.add(cat)
            db.commit()
            db.refresh(cat)
        return cat

    @staticmethod
    def create_listing(db: Session, farmer_id: int, cat_id: int, name: str, price: float, stock: int):
        return ProductRepository.create(db, farmer_id, cat_id, name, price, stock)