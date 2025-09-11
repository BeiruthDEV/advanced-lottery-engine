from typing import List, Iterable


class ExcludeRecentFilter:

    def __init__(self, recent_draws: Iterable[Iterable[int]] | None = None):
        self.recent_draws = list(recent_draws or [])
        self.excluded = set()
        for draw in self.recent_draws:
            self.excluded.update(draw)


    def apply(self, ticket: List[int]) -> List[int]:
        allowed = [n for n in ticket if n not in self.excluded]
        if not allowed:
            return ticket
        return allowed