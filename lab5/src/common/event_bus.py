from typing import Dict, List, Type, Callable, Any
import threading
import logging
from src.common.events import IntegrationEvent

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self._listeners: Dict[Type[IntegrationEvent], List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: Type[IntegrationEvent], handler: Callable[[Any], None]) -> None:
        """Реєструє підписника на конкретний тип події."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(handler)

    def publish(self, event: IntegrationEvent) -> None:
        """Публікує подію. Обробка підписниками запускається в окремому потоці (Async)."""
        event_type = type(event)
        if event_type not in self._listeners or not self._listeners[event_type]:
            return

        for handler in self._listeners[event_type]:
            # Запускаємо обробку в окремому потоці, щоб не блокувати основну операцію
            thread = threading.Thread(
                target=self._execute_handler, 
                args=(handler, event),
                name=f"EventBusHandler-{event_type.__name__}"
            )
            thread.start()

    def _execute_handler(self, handler: Callable[[Any], None], event: IntegrationEvent) -> None:
        try:
            handler(event)
        except Exception as e:
            logger.error(f"[EventBus] Error executing handler {handler.__name__} for event {type(event).__name__}: {e}")