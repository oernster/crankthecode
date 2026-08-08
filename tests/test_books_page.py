"""The books page and the catalogue entries behind it."""

from __future__ import annotations

import re

from fastapi.testclient import TestClient

from app.domain.books_catalogue import BookCatalogueEntry
from app.main import create_app


def test_books_page_renders_and_links_to_amazon_uk():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/books")
    assert resp.status_code == 200

    assert "Books" in resp.text

    # Read time is post-only; non-post pages should not render the pill.
    assert 'class="read-time-bar"' not in resp.text

    # Covers (served from /static). Support both unfingerprinted and
    # fingerprinted asset paths.
    assert re.search(
        r"/static/images/_cover_da(?:\.[0-9a-f]{8,})?\.png",
        resp.text,
    ), resp.text
    assert re.search(
        r"/static/images/_cover_da_patterns(?:\.[0-9a-f]{8,})?\.png",
        resp.text,
    ), resp.text
    assert re.search(
        r"/static/images/_cover_relativistic_da_architecture(?:\.[0-9a-f]{8,})?\.png",
        resp.text,
    ), resp.text
    assert re.search(
        r"/static/images/_cover-da-move-space(?:\.[0-9a-f]{8,})?\.png",
        resp.text,
    ), resp.text

    # Canonical Amazon UK links (no link switching).
    assert "https://www.amazon.co.uk/dp/B0GT4JNMGK" in resp.text
    assert "https://www.amazon.co.uk/dp/B0GT4CZ327" in resp.text
    assert "https://www.amazon.co.uk/dp/B0H8HTM8H3" in resp.text
    assert "https://www.amazon.co.uk/dp/B0GTDX7186" in resp.text

    # Complete series hardback compilation: rendered separately (not a 5th peer
    # card in the primary series grid).
    assert "Complete Series Edition" in resp.text
    assert "https://www.amazon.co.uk/dp/B0H8HVZKY1" in resp.text
    assert re.search(
        r"/static/images/hardback_cover(?:\.[0-9a-f]{8,})?\.png",
        resp.text,
    ), resp.text
    assert (
        "All four volumes combined into a single hardback reference edition"
        in resp.text
    )

    # Guardrail: the main series grid should remain exactly 4 tiles.
    assert resp.text.count('class="book-tile"') == 4, resp.text

    # Hover/subtitle text should be present (consistent behaviour across cards).
    assert "A Positional Model of Organisational Change" in resp.text

    # Subtitles must be visible (not hover-only) and must match hover text.
    assert re.search(
        r'class="book-title">\s*Decision Architecture\s*</div>',
        resp.text,
    ), resp.text
    assert re.search(
        r'class="book-subtitle">\s*How technical organisations fail and'
        r" recover\s*</div>",
        resp.text,
    ), resp.text

    assert re.search(
        r'class="book-title">\s*Decision Architecture: The Move Space\s*</div>',
        resp.text,
    ), resp.text
    assert re.search(
        r'class="book-subtitle">\s*A Positional Model of Organisational'
        r" Change\s*</div>",
        resp.text,
    ), resp.text

    # Source-of-truth guard: old title-case subtitle should not appear anymore.
    assert "How Technical Organisations Fail and Recover" not in resp.text


def test_book_catalogue_entry_alt_text_omits_empty_subtitle():
    entry = BookCatalogueEntry(
        title="T",
        cover_asset="images/x.png",
        amazon_uk_url="https://example.invalid",
        hover_text="",
    )
    assert entry.alt_text == "T"


def test_compilation_edition_alt_text_omits_empty_support_line():
    from app.domain.books_compilations import CompilationEdition

    edition = CompilationEdition(
        title="Decision Architecture Series",
        cover_asset="images/hardback_cover.png",
        amazon_uk_url="https://www.amazon.co.uk/dp/B0H8HVZKY1",
        support_line="",
    )
    assert edition.alt_text == "Decision Architecture Series"
