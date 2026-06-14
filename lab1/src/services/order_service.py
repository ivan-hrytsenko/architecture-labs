from typing import List, Dict
from sqlalchemy.orm import Session
from decimal import Decimal
from lab1.src.repositories.order_repository import OrderRepository
from lab1.src.repositories.product_repository import ProductRepository
from lab1.src.models.order import Order

class InsufficientStockError(Exception):
    pass

class OrderNotFoundError(Exception):
    pass

class InvalidOrderStatusError(Exception):
    pass

class OrderService:
    @staticmethod
    def place_order(db: Session, customer_id: int, items: List[Dict]) -> Order:
        if not items:
            raise ValueError("Order must contain at least one item")
        
        try:
            total = Decimal('0.00')
            validated_items = []
            
            for item in items:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                
                if not product_id or not quantity or quantity <= 0:
                    raise ValueError(f"Invalid item: {item}")
                
                product = ProductRepository.get_by_id(db, product_id)
                if not product:
                    raise ValueError(f"Product {product_id} not found")
                
                if product.stock_quantity < quantity:
                    raise InsufficientStockError(
                        f"Insufficient stock for product {product.name}. "
                        f"Available: {product.stock_quantity}, Requested: {quantity}"
                    )
                
                total += Decimal(str(product.price)) * quantity
                validated_items.append((product, quantity))
            
            order = OrderRepository.create_order_record(db, customer_id, total)
            
            for product, quantity in validated_items:
                OrderRepository.add_item_record(db, order.id, product.id, quantity, product.price)
                product.stock_quantity -= quantity
            
            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            if isinstance(e, (InsufficientStockError, ValueError)):
                raise e
            raise Exception(f"Order placement failed: {str(e)}") from e

    @staticmethod
    def complete_order(db: Session, order_id: int) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")
        if order.status == 'completed':
            raise InvalidOrderStatusError(f"Order {order_id} is already completed")
        if order.status == 'cancelled':
            raise InvalidOrderStatusError(f"Cannot complete cancelled order {order_id}")
        
        try:
            order.status = 'completed'
            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to complete order: {str(e)}") from e

    @staticmethod
    def cancel_order(db: Session, order_id: int) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")
        if order.status == 'cancelled':
            raise InvalidOrderStatusError(f"Order {order_id} is already cancelled")
        if order.status == 'completed':
            raise InvalidOrderStatusError(f"Cannot cancel completed order {order_id}")
        
        try:
            for item in order.items:
                product = ProductRepository.get_by_id(db, item.product_id)
                if product:
                    product.stock_quantity += item.quantity
            
            order.status = 'cancelled'
            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to cancel order: {str(e)}") from e