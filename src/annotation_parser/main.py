from cli_args import build_parser
from commons.langchain_for_title import get_clean_book_title
from utils.parser import build_books, associate_notes


def main() -> None:
    cli_args = build_parser()
    # annotation_lst = parse_clippings_file(cli_args.input)
    # highlights = associate_notes(annotation_lst)
    books = build_books(
        cli_args.input,
    )

    for book in books:
        book.title, book.author =get_clean_book_title(f"{book.title}-{book.author}")
        book.annotations = associate_notes(
            book.annotations,
        )
    breakpoint()
    # TODO:
    # 1. Read clipping file
    # 2. Parse annotations
    # 3. Group into books
    # 4. Merge notes
    # 5. Export markdown


if __name__ == "__main__":
    main()
