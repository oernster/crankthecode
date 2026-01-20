from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import markdown

from app.ports.markdown_renderer import MarkdownRenderer


@dataclass(frozen=True, slots=True)
class PythonMarkdownRenderer(MarkdownRenderer):
    """Markdown rendering strategy using the `markdown` library."""

    extensions: Sequence[str] = ("fenced_code", "codehilite", "tables")

    def render(self, markdown_text: str) -> str:
        return markdown.markdown(markdown_text, extensions=list(self.extensions))
