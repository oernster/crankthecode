from __future__ import annotations

from typing import Protocol


class MarkdownRenderer(Protocol):
    """Strategy port for rendering Markdown to HTML."""

    def render(self, markdown_text: str) -> str:
        """Render markdown to HTML."""
