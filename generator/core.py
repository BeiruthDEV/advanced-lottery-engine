from typing import List
from .strategies import QuickPickStrategy


class LotteryGenerator:

    def __init__(self, strategy: QuickPickStrategy):
        self.strategy = strategy


    def generate_ticket(self, filters: list | None = None, sort: bool = True) -> List[int]:
        ticket = self.strategy.generate()
        if filters:
            for f in filters:
                ticket = f.apply(ticket)
        if sort:
            try:
                ticket = sorted(ticket)
            except Exception:
                pass
        return ticket


    def generate_multiple(self, count: int = 1, **kwargs) -> List[List[int]]:
        return [self.generate_ticket(**kwargs) for _ in range(count)]