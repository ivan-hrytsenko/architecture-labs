from dataclasses import dataclass

@dataclass
class UserStats:
    total_users: int
    total_farmers: int
    total_customers: int

@dataclass
class ProductMetrics:
    total_products: int
    average_price: float