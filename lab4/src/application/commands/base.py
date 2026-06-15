from typing import TypeVar, Generic

C = TypeVar('C')
R = TypeVar('R')

class CommandHandler(Generic[C, R]):
    def handle(self, command: C) -> R:
        raise NotImplementedError