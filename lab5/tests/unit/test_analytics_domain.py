from src.analytics.domain.models import UserStats, ProductMetrics
from src.analytics.infrastructure.models import UserStatsORM, ProductMetricsORM
from src.analytics.infrastructure.mappers import AnalyticsMapper

def test_analytics_mapper_user_stats():
    orm = UserStatsORM(total_users=5, total_farmers=2, total_customers=3)
    domain = AnalyticsMapper.user_stats_to_domain(orm)
    
    assert domain.total_users == 5
    assert domain.total_farmers == 2
    assert domain.total_customers == 3

def test_analytics_mapper_empty_orm():
    domain = AnalyticsMapper.product_metrics_to_domain(None)
    assert domain.total_products == 0
    assert domain.average_price == 0.0