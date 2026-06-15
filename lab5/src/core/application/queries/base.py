from typing import TypeVar, Generic

Q = TypeVar('Q')
R = TypeVar('R')

class QueryHandler(Generic[Q, R]):
    def handle(self, query: Q) -> R:
        raise NotImplementedError