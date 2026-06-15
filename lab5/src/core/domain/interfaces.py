from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.domain.models import User, Product

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass