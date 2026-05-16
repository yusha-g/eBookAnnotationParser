from src.annotation_parser.cli_args import build_parser


def main() -> None:
    args = build_parser()
    print(args)

    # TODO:
    # 1. Read clipping file
    # 2. Parse annotations
    # 3. Group into books
    # 4. Merge notes
    # 5. Export markdown


if __name__ == "__main__":
    main()
