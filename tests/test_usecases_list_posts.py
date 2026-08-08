from __future__ import annotations

from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.assets.manifest import AssetManifest
from app.domain.models import MarkdownPost
from app.usecases.list_posts import (
    ListPostsUseCase,
    _extract_cover_image_and_strip,
    _strip_image_paragraph,
)
from tests.fakes import InMemoryPostsRepository


def test_list_posts_sorts_by_date_desc_and_renders_summary():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="old",
                title="Old",
                date="2020-01-01 12:00",
                tags=("t",),
                blurb=None,
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=(),
                content_markdown="First para\n\nSecond para",
                emoji=None,
                post_type=None,
                role=None,
            ),
            MarkdownPost(
                slug="new",
                title="New",
                date="2021-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image=None,
                thumb_image=None,
                extra_images=(),
                content_markdown="Hello\n\nMore",
                emoji=None,
                post_type=None,
                role=None,
            ),
        )
    )
    uc = ListPostsUseCase(
        repo=repo, renderer=PythonMarkdownRenderer(), assets=AssetManifest(mapping={})
    )

    result = uc.execute()

    assert [p.slug for p in result] == ["new", "old"]
    assert "<p>" in result[0].summary_html
    assert "Hello" in result[0].summary_html


def test_list_posts_prefers_frontmatter_image_as_cover_and_strips_image_paragraph():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="one",
                title="One",
                date="2021-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image="/static/images/cover.jpg",
                thumb_image=None,
                extra_images=(),
                content_markdown=(
                    "Intro\n\n" "![Banner](/static/images/cover.jpg)\n\n" "More"
                ),
                emoji=None,
                post_type=None,
                role=None,
            ),
        )
    )
    uc = ListPostsUseCase(
        repo=repo, renderer=PythonMarkdownRenderer(), assets=AssetManifest(mapping={})
    )

    result = uc.execute()
    assert len(result) == 1
    assert result[0].cover_image_url == "/static/images/cover.jpg"
    assert result[0].thumb_image_url == "/static/images/cover.jpg"
    # Summary should not include the cover image markdown.
    assert "/static/images/cover.jpg" not in result[0].summary_html


def test_list_posts_does_not_strip_cover_image_when_it_only_appears_in_body():
    """Regression test.

    Don't remove images from legitimate sections (e.g. screenshots).
    """

    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="one",
                title="One",
                date="2021-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image="/static/images/cover.jpg",
                thumb_image=None,
                extra_images=(),
                content_markdown=(
                    "Intro\n\n"
                    "## Screenshots\n\n"
                    "![Main](/static/images/cover.jpg)\n\n"
                    "More"
                ),
                emoji=None,
                post_type=None,
                role=None,
            ),
        )
    )
    uc = ListPostsUseCase(
        repo=repo, renderer=PythonMarkdownRenderer(), assets=AssetManifest(mapping={})
    )

    result = uc.execute()

    assert len(result) == 1
    # The post still uses the frontmatter image as its cover...
    assert result[0].cover_image_url == "/static/images/cover.jpg"
    # ...but the summary should keep the markdown intact if the image is not in
    # the "cover" positions (near start). In this case, the first paragraph is
    # just "Intro".
    assert "/static/images/cover.jpg" not in result[0].summary_html


def test_list_posts_prefers_thumb_image_when_provided():
    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="one",
                title="One",
                date="2021-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image="/static/images/cover.jpg",
                thumb_image="/static/images/thumb.png",
                extra_images=(),
                content_markdown="Intro\n\nMore",
                emoji=None,
                post_type=None,
                role=None,
            ),
        )
    )
    uc = ListPostsUseCase(
        repo=repo, renderer=PythonMarkdownRenderer(), assets=AssetManifest(mapping={})
    )

    result = uc.execute()

    assert result[0].cover_image_url == "/static/images/cover.jpg"
    assert result[0].thumb_image_url == "/static/images/thumb.png"


def test_cover_helpers_handle_empty_markdown_gracefully():
    cover, remaining = _extract_cover_image_and_strip("")
    assert cover is None
    assert remaining == ""

    # Stripping an image from empty content should be a no-op.
    assert _strip_image_paragraph("", "/static/images/x.png") == ""


def test_list_posts_strips_extra_image_paragraphs_from_the_summary():
    """`extra_images` render in a controlled gallery, never inline in the summary."""

    repo = InMemoryPostsRepository(
        posts=(
            MarkdownPost(
                slug="gallery",
                title="Gallery",
                date="2020-01-01 12:00",
                tags=(),
                blurb=None,
                one_liner=None,
                image="/static/images/cover.png",
                thumb_image=None,
                extra_images=("/static/images/extra.png",),
                content_markdown=(
                    "![Cover](/static/images/cover.png)\n\n"
                    "Lead paragraph.\n\n"
                    "![Extra](/static/images/extra.png)\n"
                ),
                emoji=None,
                post_type=None,
                role=None,
            ),
        )
    )

    summaries = ListPostsUseCase(
        repo=repo, renderer=PythonMarkdownRenderer(), assets=AssetManifest(mapping={})
    ).execute()

    assert len(summaries) == 1
    assert "/static/images/extra.png" not in summaries[0].summary_html


def test_strip_image_paragraph_tail_branch_covered():
    from app.usecases.list_posts import _strip_image_paragraph

    md = "Para\n\n![Alt](/static/images/cover.png)\n"
    out = _strip_image_paragraph(md, "/static/images/cover.png", tail=1)
    assert "cover.png" not in out
