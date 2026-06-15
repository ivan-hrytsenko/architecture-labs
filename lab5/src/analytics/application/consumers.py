from src.analytics.infrastructure.repositories import AnalyticsRepository

class UserRegisteredConsumer:
    def __init__(self, repo: AnalyticsRepository):
        self._repo = repo

    def execute(self, role: str) -> None:
        self._repo.update_user_counts(role=role)

class ProductCreatedConsumer:
    def __init__(self, repo: AnalyticsRepository):
        self._repo = repo

    def execute(self, price: float) -> None:
        self._repo.add_product_to_metrics(new_price=price)