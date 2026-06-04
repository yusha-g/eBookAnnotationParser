import re


SEPARATOR = "=========="

TITLE_RE = re.compile(
    r"^(?P<title>.+?)(?:\s+\((?P<author>[^()]*)\))?$"
)

TYPE_RE = re.compile(
    r"- Your (?P<type>Highlight|Note|Bookmark)"
)

LOCATION_RE = re.compile(
    r"location (?P<start>\d+)(?:-(?P<end>\d+))?"
)

PAGE_RE = re.compile(
    r"page (?P<start>\d+)(?:-(?P<end>\d+))?"
)

DATE_RE = re.compile(
    r"Added on (?P<date>[^\n]+)"
)


SERIES_RE = re.compile(
    r"\[(?P<series>.+?)\s+(?P<number>\d+)\]"
)