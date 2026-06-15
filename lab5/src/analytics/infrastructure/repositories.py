from sqlalchemy.orm import Session
from typing import Optional
from src.analytics.infrastructure.models import UserStatsORM, ProductMetricsORM
from src.analytics.domain.models import UserStats, ProductMetrics
from src.analytics.infrastructure.mappers import AnalyticsMapper  # ДОДАНО

class AnalyticsRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_user_stats(self) -> UserStats:
        orm = self._session.query(UserStatsORM).filter_by(id=1).first()
        return AnalyticsMapper.user_stats_to_domain(orm)  # ВИКОРИСТОВУЄТЬСЯ МАПЕР

    def get_product_metrics(self) -> ProductMetrics:
        orm = self._session.query(ProductMetricsORM).filter_by(id=1).first()
        return AnalyticsMapper.product_metrics_to_domain(orm)  # ВИКОРИСТОВУЄТЬСЯ МАПЕР

    def update_user_counts(self, role: str) -> None:
        orm = self._session.query(UserStatsORM).filter_by(id=1).first()
        if not orm:
            orm = UserStatsORM(id=1, total_users=0, total_farmers=0, total_customers=0)
            self._session.add(orm)
        
        orm.total_users += 1
        if role.lower() == "farmer":
            orm.total_farmers += 1
        else:
            orm.total_customers += 1
        self._session.commit()

    def add_product_to_metrics(self, new_price: float) -> None:
        orm = self._session.query(ProductMetricsORM).filter_by(id=1).first()
        if not orm:
            orm = ProductMetricsORM(id=1, total_products=0, average_price=0.0)
            self._session.add(orm)

        current_total = orm.total_products
        current_avg = orm.average_price

        orm.total_products += 1
        orm.average_price = ((current_avg * current_total) + new_price) / orm.total_products
        self._session.commit()