from src.core.domain.models import User, Product
from src.core.infrastructure.models import UserORM, ProductORM
from src.core.domain.factory import DomainFactory

class DataMapper:
    @staticmethod
    def user_to_orm(domain: User) -> UserORM:
        if not domain:
            return None
        return UserORM(
            id=domain.id,
            username=domain.username,
            email=domain.email,
            role=domain.role
        )

    @staticmethod
    def user_to_domain(orm: UserORM) -> User:
        if not orm:
            return None
        return DomainFactory.create_user(
            id=orm.id,
            username=orm.username,
            email=orm.email,
            role=orm.role
        )

    @staticmethod
    def product_to_orm(domain: Product) -> ProductORM:
        if not domain:
            return None
        return ProductORM(
            id=domain.id,
            title=domain.title,
            description=domain.description,
            price=domain.price.value,
            quantity=domain.quantity.value,
            farmer_id=domain.farmer_id
        )

    @staticmethod
    def product_to_domain(orm: ProductORM) -> Product:
        if not orm:
            return None
        return DomainFactory.create_product(
            orm.id,
            orm.title,
            orm.description,
            orm.price,
            orm.quantity,
            orm.farmer_id
        )