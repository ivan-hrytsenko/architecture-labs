from abc import ABC, abstractmethod

class NotificationComponent(ABC):
    @abstractmethod
    def send_welcome_notification(self, email: str, username: str) -> None:
        """Надсилає сповіщення новому зареєстрованому користувачу."""
        pass

    @abstractmethod
    def send_product_created_notification(self, title: str, price: float) -> None:
        """Сповіщає систему/користувачів про появу нового товару."""
        pass