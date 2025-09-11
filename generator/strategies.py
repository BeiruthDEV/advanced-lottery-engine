from typing import List
from .utils import make_rng
import random


class QuickPickStrategy:
    

    def __init__(
        self,
        pool_min: int = 1,
        pool_max: int = 60,
        numbers_per_ticket: int = 6,
        seed: str | None = None,
        secure: bool = True,
    ):
        self.pool_min = pool_min
        self.pool_max = pool_max
        self.n = numbers_per_ticket
        self.rng = make_rng(seed, secure)

    def generate(self) -> List[int]:
        pool = list(range(self.pool_min, self.pool_max + 1))
        ticket = self.rng.sample(pool, k=self.n)
        return ticket


class WeightedStrategy(QuickPickStrategy):
    

    def __init__(self, weights: dict[int, float] | None = None, **kwargs):
        super().__init__(**kwargs)
        self.weights = weights or {}

    def generate(self) -> List[int]:
        pool = list(range(self.pool_min, self.pool_max + 1))

        if not self.weights:
            return super().generate()

        weights = [self.weights.get(num, 1.0) for num in pool]
        chosen = random.choices(pool, weights=weights, k=self.n)

        # garantir unicidade (se houver duplicatas, completar com sample)
        chosen = list(dict.fromkeys(chosen))
        while len(chosen) < self.n:
            extra = self.rng.sample([x for x in pool if x not in chosen], k=1)
            chosen.extend(extra)

        return chosen
