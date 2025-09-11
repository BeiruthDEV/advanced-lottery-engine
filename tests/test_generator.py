from generator.strategies import QuickPickStrategy, WeightedStrategy
from generator.core import LotteryGenerator


def test_quickpick_length():
    s = QuickPickStrategy(
        pool_min=1,
        pool_max=10,
        numbers_per_ticket=5,
        seed="testseed",
        secure=False,
    )
    gen = LotteryGenerator(s)
    t = gen.generate_ticket()

    assert len(t) == 5
    assert all(1 <= n <= 10 for n in t)


def test_multiple_tickets_unique_within():
    s = QuickPickStrategy(
        pool_min=1,
        pool_max=20,
        numbers_per_ticket=6,
        seed="abc",
        secure=False,
    )
    gen = LotteryGenerator(s)
    tickets = gen.generate_multiple(10)

    for t in tickets:
        assert len(set(t)) == len(t)


# Novos testes para WeightedStrategy
def test_weighted_strategy_bias():
    weights = {7: 10.0}  # número 7 deve aparecer mais vezes
    s = WeightedStrategy(
        pool_min=1,
        pool_max=10,
        numbers_per_ticket=6,
        seed="biasseed",
        secure=False,
        weights=weights,
    )
    gen = LotteryGenerator(s)
    tickets = gen.generate_multiple(50)

    count_7 = sum(7 in t for t in tickets)
    assert count_7 > 0


def test_weighted_strategy_unique_numbers():
    weights = {i: 1.0 for i in range(1, 11)}
    s = WeightedStrategy(
        pool_min=1,
        pool_max=10,
        numbers_per_ticket=6,
        seed="uniqueseed",
        secure=False,
        weights=weights,
    )
    gen = LotteryGenerator(s)
    ticket = gen.generate_ticket()

    assert len(ticket) == len(set(ticket))
