from dataclasses import dataclass
from src.domain.interfaces import UserRepository
from src.domain.factory import DomainFactory
from src.domain.exceptions import InvariantViolationError
from src.application.commands.base import CommandHandler

@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    email: str
    role: str

class RegisterUserHandler(CommandHandler[RegisterUserCommand, int]):
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def handle(self, command: RegisterUserCommand) -> int:
        existing_user = self._user_repo.get_by_email(command.email)
        if existing_user:
            raise InvariantViolationError("User with this email already exists")

        user = DomainFactory.create_user(
            id=None,
            username=command.username,
            email=command.email,
            role=command.role
        )
        saved_user = self._user_repo.save(user)
        return saved_user.id