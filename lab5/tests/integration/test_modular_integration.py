import pytest
from src.presentation.dependencies import get_event_bus
from src.analytics.acl import AnalyticsACL
from src.analytics.infrastructure.repositories import AnalyticsRepository
from src.core.domain.events.user_events import UserRegisteredEvent
from src.core.domain.events.product_events import ProductCreatedEvent

def test_acl_intercepts_core_events_and_builds_projections(test_db_setup, db_session):
    event_bus = get_event_bus()
    acl = AnalyticsACL(session_factory=test_db_setup)
    acl.register_subscriptions(event_bus)
    repo = AnalyticsRepository(db_session)
    
    user_event_1 = UserRegisteredEvent(user_id=1, username="farmer_jon", email="jon@ex.com", role="farmer")
    user_event_2 = UserRegisteredEvent(user_id=2, username="buyer_ann", email="ann@ex.com", role="customer")
    
    event_bus.publish(user_event_1)
    event_bus.publish(user_event_2)
    
    user_stats = repo.get_user_stats()
    assert user_stats.total_users == 2
    assert user_stats.total_farmers == 1
    assert user_stats.total_customers == 1
    
    product_event_1 = ProductCreatedEvent(product_id=10, title="Milk", price=40.0, quantity=5, farmer_id=1)
    product_event_2 = ProductCreatedEvent(product_id=11, title="Cheese", price=120.0, quantity=2, farmer_id=1)
    
    event_bus.publish(product_event_1)
    event_bus.publish(product_event_2)
    
    product_metrics = repo.get_product_metrics()
    assert product_metrics.total_products == 2
    assert product_metrics.average_price == 80.0