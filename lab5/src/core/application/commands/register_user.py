import logging
from dataclasses import dataclass
from src.core.domain.interfaces import UserRepository
from src.core.domain.factory import DomainFactory
from src.core.domain.exceptions import InvariantViolationError
from src.core.application.commands.base import CommandHandler
from src.common.event_bus import EventBus
from src.core.domain.events.user_events import UserRegisteredEvent

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    email: str
    role: str

class RegisterUserHandler(CommandHandler[RegisterUserCommand, int]):
    def __init__(
        self, 
        user_repo: UserRepository, 
        notification_service: NotificationComponent,
        event_bus: EventBus,
        mode: str = "sync"
    ):
        self._user_repo = user_repo
        self._notification_service = notification_service
        self._event_bus = event_bus
        self._mode = mode

    def handle(self, command: RegisterUserCommand) -> int:
        existing_user = self._user_repo.get_by_email(command.email)
        if existing_user:
            raise InvariantViolationError("User with this email already exists")

        user = DomainFactory.create_user(
            None,
            command.username,
            command.email,
            command.role
        )
        saved_user = self._user_repo.save(user)

        if self._mode == "sync":
            try:
                self._notification_service.send_welcome_notification(
                    email=saved_user.email,
                    username=saved_user.username
                )
            except Exception as e:
                logger.error(f"[Sync Notification Error] Failed to send welcome email: {e}")
                if hasattr(self._user_repo, "delete"):
                    self._user_repo.delete(saved_user.id)
                raise InvariantViolationError("Registration aborted due to notification system failure")
        
        elif self._mode == "async":
            event = UserRegisteredEvent(
                user_id=saved_user.id,
                username=saved_user.username,
                email=saved_user.email,
                role=saved_user.role
            )
            self._event_bus.publish(event)

        return saved_user.id