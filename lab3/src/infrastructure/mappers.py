from src.domain.models import User, Product
from src.domain.value_objects import Price, Quantity
from src.infrastructure.models import UserORM, ProductORM

class DataMapper:
    @staticmethod
    def user_to_domain(orm: UserORM) -> User:
        if not orm:
            return None
        return User(id=orm.id, username=orm.username, email=orm.email, role=orm.role)

    @staticmethod
    def user_to_orm(domain: User) -> UserORM:
        if not domain:
            return None
        return UserORM(id=domain.id, username=domain.username, email=domain.email, role=domain.role)

    @staticmethod
    def product_to_domain(orm: ProductORM) -> Product:
        if not orm:
            return None
        return Product(
            id=orm.id,
            title=orm.title,
            description=orm.description,
            price=Price(orm.price),
            quantity=Quantity(orm.quantity),
            farmer_id=orm.farmer_id
        )

    @staticmethod
    def product_to_orm(domain: Product) -> ProductORM:
        if not domain:
            return None
        return ProductORM(
            id=domain.id,
            title=domain.title,
            description=domain.description,
            price=domain.price.amount,
            quantity=domain.quantity.value,
            farmer_id=domain.farmer_id
        )