from __future__ import annotations

from app.usecases.get_post import _extract_markdown_sections


def test_extract_markdown_sections_removes_screenshots_section_and_returns_its_body():
    md = """Intro

## Screenshots

![One](/static/images/one.png)

## Rationale

Some text.
"""

    remaining, bodies = _extract_markdown_sections(md, title="Screenshots")

    assert "## Screenshots" not in remaining
    assert "## Rationale" in remaining
    assert len(bodies) == 1
    assert "![One](/static/images/one.png)" in bodies[0]


def test_extract_markdown_sections_is_case_insensitive_and_tolerates_indent():
    md = """Intro

    ## SCREENSHOTS

    ![One](/static/images/one.png)

## Rationale

Some text.
"""
    remaining, bodies = _extract_markdown_sections(md, title="Screenshots")
    assert "SCREENSHOTS" not in remaining
    assert len(bodies) == 1


def test_extract_markdown_sections_skips_matching_heading_with_empty_body():
    # A heading matching the title but with no body before the next same-level
    # heading is removed without contributing an (empty) body entry.
    md = "\n".join(
        [
            "Intro",
            "",
            "## Screenshots",
            "## Rationale",
            "",
            "Body text.",
        ]
    )

    remaining, bodies = _extract_markdown_sections(md, title="Screenshots")

    assert "## Screenshots" not in remaining
    assert "## Rationale" in remaining
    assert bodies == []
