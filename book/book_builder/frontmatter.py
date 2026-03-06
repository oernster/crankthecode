from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import yaml

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True, slots=True)
class Frontmatter:
    """Parsed YAML frontmatter plus remaining markdown body."""

    meta: dict[str, Any]
    body: str


def parse_frontmatter(markdown: str) -> Frontmatter:
    """Split a markdown document into (frontmatter meta, body).

    If the document has no YAML frontmatter header, `meta` is empty and `body`
    is the full original markdown.
    """

    match = _FRONTMATTER_RE.match(markdown or "")
    if not match:
        return Frontmatter(meta={}, body=markdown or "")

    meta = yaml.safe_load(match.group(1))
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        # Defensive: frontmatter should be a mapping.
        meta = {}

    body = (markdown or "")[match.end() :]
    return Frontmatter(meta=dict(meta), body=body)
