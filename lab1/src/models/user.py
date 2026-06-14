from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from lab1.src.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime)
    deleted_at = Column(DateTime, nullable=True)

    products = relationship("Product", back_populates="farmer")
    orders = relationship("Order", back_populates="customer")