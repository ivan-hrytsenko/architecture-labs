from src.analytics.domain.models import UserStats, ProductMetrics
from src.analytics.infrastructure.models import UserStatsORM, ProductMetricsORM

class AnalyticsMapper:
    @staticmethod
    def user_stats_to_domain(orm: UserStatsORM) -> UserStats:
        if not orm:
            return UserStats(total_users=0, total_farmers=0, total_customers=0)
        return UserStats(
            total_users=orm.total_users,
            total_farmers=orm.total_farmers,
            total_customers=orm.total_customers
        )

    @staticmethod
    def product_metrics_to_domain(orm: ProductMetricsORM) -> ProductMetrics:
        if not orm:
            return ProductMetrics(total_products=0, average_price=0.0)
        return ProductMetrics(
            total_products=orm.total_products,
            average_price=orm.average_price
        )