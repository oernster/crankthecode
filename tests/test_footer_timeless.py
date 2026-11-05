"""The site footer is timeless: it names the author and never a year.

The site is published on GitHub Pages, where every page is timeless by rule.
The footer is on every page, so a year there would date the whole site.
"""

from __future__ import annotations

import re

from fastapi.testclient import TestClient

from app.main import create_app

_FOOTER = re.compile(r'<div class="site-footer".*?</div>', re.S)
_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")


def _footer(path: str) -> str:
    resp = TestClient(create_app()).get(path)
    assert resp.status_code == 200, path
    match = _FOOTER.search(resp.text)
    assert match, path
    return match.group(0)


def test_footer_names_the_author_without_a_year():
    for path in ("/", "/books", "/essays"):
        footer = _footer(path)
        assert "Oliver Ernster" in footer, path
        assert not _YEAR.search(footer), footer
