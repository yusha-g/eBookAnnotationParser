import argparse
from pathlib import Path


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="annotation-parser",
        description=(
            "Convert Kindle My Clippings.txt exports into structured Markdown files."
        ),
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Path to the My Clippings.txt file exported from Kindle.",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("./output"),
        help="Directory to save the generated Markdown files.",
    )

    return parser


def validate_args(args: argparse.Namespace) -> None:
    if not args.input.is_file():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    if not args.output.exists():
        args.output.mkdir(parents=True, exist_ok=True)


def build_parser() -> argparse.Namespace:
    cli_args = parse_args().parse_args()
    validate_args(cli_args)

    print("Configuration:")
    print(f"Input: {cli_args.input}")
    print(f"Output: {cli_args.output}")
    return cli_args
