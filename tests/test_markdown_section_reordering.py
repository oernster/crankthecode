from __future__ import annotations

from app.usecases.get_post import (
    _extract_markdown_sections,
    _insert_screenshots_after_problem_solution_impact,
)


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


def test_insert_screenshots_after_problem_solution_impact_inserts_after_that_section():
    md = """Intro

## Problem -> Solution -> Impact

Problem paragraph.

Solution paragraph.

Impact paragraph.

## Rationale

Some text.
"""

    screenshots = """## Screenshots

![One](/static/images/one.png)
"""

    out = _insert_screenshots_after_problem_solution_impact(
        md,
        screenshots_markdown=screenshots,
    )

    assert out.index("## Problem") < out.index("## Screenshots")
    assert out.index("## Screenshots") < out.index("## Rationale")


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

