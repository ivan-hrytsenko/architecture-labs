from dataclasses import dataclass
from typing import List
from sqlalchemy.orm import Session
from src.infrastructure.models import ProductORM
from src.application.queries.read_models import ProductReadModel
from src.application.queries.base import QueryHandler

@dataclass(frozen=True)
class GetAllProductsQuery:
    pass

class GetAllProductsHandler(QueryHandler[GetAllProductsQuery, List[ProductReadModel]]):
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def handle(self, query: GetAllProductsQuery) -> List[ProductReadModel]:
        products_orm = self._db_session.query(ProductORM).all()
        return [
            ProductReadModel(
                id=p.id,
                title=p.title,
                description=p.description,
                price=p.price,
                quantity=p.quantity,
                farmer_id=p.farmer_id
            )
            for p in products_orm
        ]