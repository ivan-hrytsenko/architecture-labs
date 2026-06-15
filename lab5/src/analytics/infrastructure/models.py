from sqlalchemy import Column, Integer, Float
from src.common.database import Base

class UserStatsORM(Base):
    __tablename__ = "analytics_user_stats"

    id = Column(Integer, primary_key=True, default=1)
    total_users = Column(Integer, default=0)
    total_farmers = Column(Integer, default=0)
    total_customers = Column(Integer, default=0)

class ProductMetricsORM(Base):
    __tablename__ = "analytics_product_metrics"

    id = Column(Integer, primary_key=True, default=1)
    total_products = Column(Integer, default=0)
    average_price = Column(Float, default=0.0)