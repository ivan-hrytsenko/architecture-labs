from sqlalchemy.orm import Session
from lab1.src.models.order import Order, OrderItem

class OrderRepository:
    @staticmethod
    def create_order_record(db: Session, customer_id: int, total) -> Order:
        order = Order(customer_id=customer_id, total_amount=total, status='pending')
        db.add(order)
        db.flush()
        return order

    @staticmethod
    def add_item_record(db: Session, order_id: int, product_id: int, qty: int, price) -> OrderItem:
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=qty,
            price_at_purchase=price
        )
        db.add(item)
        db.flush()
        return item

    @staticmethod
    def get_by_id(db: Session, order_id: int) -> Order:
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def get_by_customer(db: Session, customer_id: int, limit: int = 10, offset: int = 0):
        return db.query(Order)\
            .filter(Order.customer_id == customer_id)\
            .order_by(Order.created_at.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()