from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from hashlib import md5

class AnnotationType(str, Enum):
    HIGHLIGHT = "Highlight"
    NOTE = "Note"

@dataclass
class Annotation:
    annotation_type: AnnotationType

    content: str

    created_at: datetime

    location_start: int
    location_end: int

    page_start: int | None = None
    page_end: int | None = None

    associated_note: str | None = None

@dataclass
class Series:
    name: str
    number: int

@dataclass
class Book:
    title: str
    author: str
    annotations: list[Annotation]
    series: Series | None = None

    id: str = field(init=False)

    def add_annotation(self, annotation: Annotation) -> None:
        self.annotations.append(annotation)

    
    def generate_id(self) -> str:
        normalise = (
            f"{self.title.strip().lower()}::"
            f"{(self.author or '').strip().lower()}"
        )

        return md5(normalise.encode("utf-8")).hexdigest()

    def __post_init__(self) -> None:
        """Automatically generate and assign the `id` after dataclass init."""
        self.id = self.generate_id()