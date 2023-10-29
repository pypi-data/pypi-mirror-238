import argparse
from cProfile import Profile
from dataclasses import dataclass

import chessy.core.atkgen as ca
import chessy.core.board as cb
import chessy.core.evaluator as ce


@dataclass(frozen=True, slots=True)
class CliArgs:
    fen: str
    depth: int
    output: str | None


def parse_cli_args() -> CliArgs:
    parser = argparse.ArgumentParser(description="chessy move search profiler")
    parser.add_argument(
        "fen",
        help="The initial FEN to be used during the calculations.",
        metavar="FEN",
    )
    parser.add_argument(
        "depth", help="The depth to be used during the calculations.", type=int
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file. If unspecified, prints to stdout instead.",
    )
    args = parser.parse_args()
    return CliArgs(fen=args.fen, depth=args.depth, output=args.output)


def main() -> None:
    args = parse_cli_args()
    fen = args.fen
    depth = args.depth
    output = args.output

    # Create engine and its params outside `calc` so startup time isn't considered by
    # the profiler.
    ca.force_init_all_tables()
    board = cb.Board.from_fen(fen)
    evaluator = ce.Evaluator()

    def calc(depth: int) -> None:
        evaluator.start_search(board, max_depth=depth)

    p = Profile()
    p.runcall(calc, depth)
    if output is None:
        p.print_stats(sort="cumulative")
    else:
        p.dump_stats(output)


if __name__ == "__main__":
    main()
