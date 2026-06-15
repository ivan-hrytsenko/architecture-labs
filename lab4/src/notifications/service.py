import logging
from src.notifications.interface import NotificationComponent

logger = logging.getLogger(__name__)

class NotificationService(NotificationComponent):
    def __init__(self, fail_safely: bool = False):
        # Якщо fail_safely=True, компонент буде імітувати критичний збій (наприклад, таймаут мережі)
        self._fail_safely = fail_safely

    def send_welcome_notification(self, email: str, username: str) -> None:
        if self._fail_safely:
            raise RuntimeWarning("SMTP Server connection timeout! Failed to send email.")
        
        logger.info(f"[NOTIFICATION] Welcome email sent to {username} ({email}) successfully.")

    def send_product_created_notification(self, title: str, price: float) -> None:
        if self._fail_safely:
            raise RuntimeWarning("Notification broker is offline! Failed to broadcast product.")
            
        logger.info(f"[NOTIFICATION] Broadcast: New product '{title}' is now available for {price} UAH!")