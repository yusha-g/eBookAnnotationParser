from bdb import Breakpoint
from datetime import datetime
from pathlib import Path
from turtle import title

from commons.constants import SEPARATOR, DATE_RE, LOCATION_RE, PAGE_RE, TITLE_RE, TYPE_RE
from commons.models import Annotation, AnnotationType, Book

def note_matches_highlight(
    note: Annotation,
    highlight: Annotation,
) -> bool:
    """
    Determine whether a note belongs to a highlight.

    Matching priority:
    1. Location-based matching (preferred)
    2. Page-based matching (fallback)
    """

    # Location-based matching
    if (
        note.location_start is not None
        and highlight.location_start is not None
        and highlight.location_end is not None
    ):
        return (
            highlight.location_start
            <= note.location_start
            <= highlight.location_end
        )

    # Page-based matching
    if (
        note.page_start is not None
        and highlight.page_start is not None
    ):
        note_page_end = note.page_end or note.page_start
        highlight_page_end = (
            highlight.page_end or highlight.page_start
        )

        return not (
            note_page_end < highlight.page_start
            or note.page_start > highlight_page_end
        )

    return False

def associate_notes(
    annotations: list[Annotation],
) -> list[Annotation]:
    notes = [
        a
        for a in annotations
        if a.annotation_type == AnnotationType.NOTE
    ]

    highlights = [
        a
        for a in annotations
        if a.annotation_type == AnnotationType.HIGHLIGHT
    ]

    for highlight in highlights:
        candidates = [
            note
            for note in notes
            if note_matches_highlight(
                note,
                highlight,
            )
        ]

        if candidates:
            latest_note = max(
                candidates,
                key=lambda note: note.created_at,
            )

            highlight.associated_note = (
                latest_note.content
            )

    return highlights

def parse_raw_clipping(block: str) -> tuple[Book, Annotation]:
    lines = block.strip().splitlines()
    title_line = lines[0]

    title_match = TITLE_RE.search(title_line)
    if not title_match:
        raise ValueError(
            f"Could not parse title:\n{title_line}"
        )

    metadata = Book(**title_match.groupdict())

    type_match = TYPE_RE.search(block)
    if not type_match:
        raise ValueError(f"Could not parse annotation type:\n{block}")

    date_match = DATE_RE.search(block)
    if not date_match:
        raise ValueError(f"Could not parse date:\n{block}")

    annotation_type = AnnotationType(
        type_match.group("type")
    )

    created_at = datetime.strptime(
        date_match.group("date"),
        "%A, %d %B %Y %H:%M:%S",
    )

    location_start = None
    location_end = None
    location_match = LOCATION_RE.search(block)
    if location_match:
        location_start = int(location_match.group("start"))
        location_end = int(
            location_match.group("end") or location_start
        )

    page_start = None
    page_end = None

    page_match = PAGE_RE.search(block)
    if page_match:
        page_start = int(page_match.group("start"))
        page_end = int(
            page_match.group("end") or page_start
        )

    lines = block.strip().splitlines()

    content = "\n".join(lines[3:]).strip()

    annotation= Annotation(
        annotation_type=annotation_type,
        content=content,
        created_at=created_at,
        location_start=location_start,
        location_end=location_end,
        page_start=page_start,
        page_end=page_end,
    )

    return metadata, annotation

def build_books(
    path: Path,
) -> list[Book]:
    text = path.read_text(
        encoding="utf-8-sig",
    )

    books: dict[
        tuple[str, str],
        Book,
    ] = {}

    for block in text.split(SEPARATOR):
        if not block.strip():
            continue

        metadata, annotation = (
            parse_raw_clipping(block)
        )

        key = (
            metadata.title,
            metadata.author,
        )

        if key not in books:
            books[key] = Book(
                title=metadata.title,
                author=metadata.author,
                series=metadata.series,
                annotations=[],
            )

        books[key].add_annotation(
            annotation
        )

    return list(books.values())

# def parse_clippings_file(path: Path) -> list[Annotation]:
#     text = path.read_text(
#         encoding="utf-8-sig",
#     )

#     blocks = text.split(SEPARATOR)

#     return [
#         parse_raw_clipping(block)
#         for block in blocks
#         if block.strip()
#     ]