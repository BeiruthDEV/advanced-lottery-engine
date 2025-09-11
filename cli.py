import argparse
import yaml
from generator.core import LotteryGenerator
from generator.strategies import QuickPickStrategy, WeightedStrategy


def main():
    parser = argparse.ArgumentParser(
        description="Gerador de apostas de loteria"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    
    generate_parser = subparsers.add_parser(
        "generate", help="Gerar apostas de loteria"
    )
    generate_parser.add_argument(
        "--tickets", type=int, default=1, help="Quantidade de jogos"
    )
    generate_parser.add_argument(
        "--strategy", choices=["quickpick", "weighted"], default="quickpick",
        help="Estratégia de geração"
    )
    generate_parser.add_argument(
        "--seed", type=str, default=None, help="Seed para geração reprodutível"
    )
    generate_parser.add_argument(
        "--secure", action="store_true", help="Usar gerador seguro (secrets)"
    )

    args = parser.parse_args()

    
    try:
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        config = {}

    
    if args.strategy == "quickpick":
        quickpick_cfg = config.get("quickpick", {})
        strategy = QuickPickStrategy(
            pool_min=quickpick_cfg.get("pool_min", 1),
            pool_max=quickpick_cfg.get("pool_max", 60),
            numbers_per_ticket=quickpick_cfg.get("numbers_per_ticket", 6),
            seed=args.seed,
            secure=args.secure,
        )
    else:  
        weighted_cfg = config.get("weighted", {})
        strategy = WeightedStrategy(
            pool_min=weighted_cfg.get("pool_min", 1),
            pool_max=weighted_cfg.get("pool_max", 60),
            numbers_per_ticket=weighted_cfg.get("numbers_per_ticket", 6),
            weights=weighted_cfg.get("weights", {}),
            seed=args.seed,
            secure=args.secure,
        )

    generator = LotteryGenerator(strategy)

    
    tickets = generator.generate_multiple(args.tickets)
    for i, t in enumerate(tickets, start=1):
        print(f"Jogo {i}: {sorted(t)}")


if __name__ == "__main__":
    main()
