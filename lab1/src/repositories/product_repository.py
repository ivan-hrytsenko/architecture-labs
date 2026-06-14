from sqlalchemy.orm import Session
from lab1.src.models.product import Product

class ProductRepository:
    @staticmethod
    def create(db: Session, farmer_id, cat_id, name, price, stock):
        product = Product(farmer_id=farmer_id, category_id=cat_id, name=name, price=price, stock_quantity=stock)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()