from sqlalchemy.orm import Session
from dataclasses import dataclass
from src.analytics.infrastructure.repositories import AnalyticsRepository

@dataclass
class GetAnalyticsReportQuery:
    pass

class GetAnalyticsReportHandler:
    def __init__(self, session: Session):
        self._session = session

    def execute(self, query: GetAnalyticsReportQuery) -> dict:
        repo = AnalyticsRepository(self._session)
        user_stats = repo.get_user_stats()
        product_metrics = repo.get_product_metrics()
        
        return {
            "users": {
                "total_users": user_stats.total_users,
                "total_farmers": user_stats.total_farmers,
                "total_customers": user_stats.total_customers
            },
            "products": {
                "total_products": product_metrics.total_products,
                "average_price": round(product_metrics.average_price, 2)
            }
        }