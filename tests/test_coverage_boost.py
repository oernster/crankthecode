from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.domain.models import MarkdownPost, PostSummary
from app.main import create_app


def _mk_summary(
    *,
    slug: str,
    title: str,
    date: str,
    tags: tuple[str, ...] = (),
    cover: str | None = None,
    thumb: str | None = None,
) -> PostSummary:
    return PostSummary(
        slug=slug,
        title=title,
        date=date,
        tags=tags,
        blurb=None,
        one_liner=None,
        cover_image_url=cover,
        thumb_image_url=thumb,
        emoji=None,
        summary_html="",
    )


def test_filesystem_posts_repository_load_file_falls_back_to_utf8_sig(monkeypatch):
    """Covers the UTF-8 BOM fallback branch in `_load_file()`."""

    from app.adapters.filesystem_posts_repository import FilesystemPostsRepository

    md = (
        "---\n"
        "title: 'Hello'\n"
        "date: '2026-01-01'\n"
        "tags: ['x']\n"
        "---\n\n"
        "Body\n"
    )

    calls: list[str] = []

    def fake_read_text(self: Path, *, encoding: str):  # type: ignore[override]
        calls.append(encoding)
        if encoding == "utf-8":
            # Simulate the first decode failing.
            raise UnicodeDecodeError("utf-8", b"\\xff", 0, 1, "boom")
        assert encoding == "utf-8-sig"
        return md

    monkeypatch.setattr(Path, "read_text", fake_read_text)
    post = FilesystemPostsRepository._load_file(Path("dummy.md"))

    assert calls == ["utf-8", "utf-8-sig"]
    assert post.slug == "dummy"
    assert post.title == "Hello"
    # Date-only normalization assumes midday.
    assert post.date == "2026-01-01 12:00"


def test_html_homepage_leadership_section_is_present_and_ordered(monkeypatch):
    """Homepage should render the Leadership menu and keep it newest-first."""

    posts = (
        _mk_summary(
            slug="lead9",
            title="Leadership Nine",
            date="2026-02-09 10:10",
            tags=("cat:Leadership",),
        ),
        _mk_summary(
            slug="lead1",
            title="Leadership One",
            date="2026-02-07 10:10",
            tags=("cat:Leadership",),
        ),
        _mk_summary(
            slug="why-crank",
            title="Why Crank?",
            date="2026-01-18 11:00",
            tags=("post",),
        ),
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert "Leadership" in resp.text

    # Ensure the series is ordered lead9 -> lead1 (newest-first for the series).
    idx_lead9 = resp.text.index("Leadership Nine")
    idx_lead1 = resp.text.index("Leadership One")
    assert idx_lead9 < idx_lead1


def test_posts_index_excludes_about_me_from_all_lists(monkeypatch):
    posts = (
        _mk_summary(
            slug="about-me",
            title="About Me",
            date="2026-01-18 07:35",
            tags=("about",),
        ),
        _mk_summary(
            slug="axisdb",
            title="AxisDB",
            date="2026-01-19 10:00",
            tags=("db",),
        ),
        _mk_summary(
            slug="stellody",
            title="Stellody",
            date="2026-01-19 13:45",
            tags=("desktop",),
        ),
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?exclude_blog=1")
    assert resp.status_code == 200
    assert "About Me" not in resp.text


def test_posts_index_excludes_axisdb_from_tools_category_view(monkeypatch):
    posts = (
        _mk_summary(
            slug="axisdb",
            title="AxisDB",
            date="2026-01-19 10:00",
            # AxisDB is not tagged as a Tools category post.
            tags=("db",),
        ),
        _mk_summary(
            slug="stellody",
            title="Stellody",
            date="2026-01-19 13:45",
            tags=("desktop", "cat:Tools"),
        ),
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?q=cat:Tools")
    assert resp.status_code == 200
    assert "AxisDB" not in resp.text
    assert "Stellody" in resp.text


def test_battlestation_page_renders(monkeypatch):
    # Ensure this route is hit for coverage.
    class FakeBlog:
        def list_posts(self):
            return ()

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)
    resp = client.get("/battlestation")
    assert resp.status_code == 200
    assert "My battlestation" in resp.text


def test_get_post_helper_functions_cover_empty_and_fallback_paths():
    from app.usecases.get_post import (
        _extract_markdown_sections,
        _has_problem_solution_impact_section,
        _insert_screenshots_after_problem_solution_impact,
    )

    assert _extract_markdown_sections("", title="Screenshots") == ("", [])
    assert _has_problem_solution_impact_section("") is False

    # Empty screenshots: no changes.
    assert (
        _insert_screenshots_after_problem_solution_impact("abc", screenshots_markdown="")
        == "abc"
    )

    # Empty markdown but screenshots provided: should return screenshots with newline.
    s = _insert_screenshots_after_problem_solution_impact(
        "", screenshots_markdown="## Screenshots\n- one"
    )
    assert s.startswith("## Screenshots")

    # Fallback append: no PSI heading found.
    s2 = _insert_screenshots_after_problem_solution_impact(
        "# Title\n\nIntro\n", screenshots_markdown="## Screenshots\n- two"
    )
    assert s2.strip().endswith("- two")


def test_insert_screenshots_inserts_after_problem_solution_impact_heading():
    from app.usecases.get_post import _insert_screenshots_after_problem_solution_impact

    md = (
        "## Problem → Solution → Impact\n"
        "\n"
        "Some content\n"
        "\n"
        "## Next\n"
        "More\n"
    )
    screenshots = "## Screenshots\n\n![x](/static/images/x.png)"
    out = _insert_screenshots_after_problem_solution_impact(md, screenshots_markdown=screenshots)

    # Should be inserted before the next heading.
    assert out.index("## Screenshots") < out.index("## Next")
    assert "/static/images/x.png" in out


def test_insert_screenshots_when_problem_solution_impact_is_last_section():
    """Covers the branch where PSI is the final heading (no following heading)."""

    from app.usecases.get_post import _insert_screenshots_after_problem_solution_impact

    md = (
        "## Problem -> Solution -> Impact\n"
        "\n"
        "Some content\n"
        "More content\n"
    )
    screenshots = "## Screenshots\n\n![x](/static/images/x.png)"
    out = _insert_screenshots_after_problem_solution_impact(md, screenshots_markdown=screenshots)
    assert out.strip().endswith("/static/images/x.png)")


def test_get_post_usecase_injects_screenshots_dedupes_and_retains_embedded_screenshots():
    from app.usecases.get_post import GetPostUseCase

    class IdentityRenderer:
        def render(self, markdown_text: str) -> str:
            return markdown_text

    class FakeRepo:
        def __init__(self, post: MarkdownPost):
            self._post = post

        def list_posts(self):
            return (self._post,)

        def get_post(self, slug: str):
            return self._post if slug == self._post.slug else None

    md_with_psi = (
        "## Problem -> Solution -> Impact\n\n"
        "Some content\n\n"
        "## Next\n\n"
        "More\n"
    )
    post = MarkdownPost(
        slug="demo",
        title="Demo",
        date="2026-01-01 12:00",
        tags=("x",),
        blurb=None,
        one_liner="a project",  # makes it a project-like post
        image="/static/images/a.png",
        thumb_image=None,
        emoji=None,
        social_image=None,
        # Includes an empty-string URL to hit the `if not url: continue` branch,
        # plus a duplicate to hit the de-dupe branch.
        extra_images=(
            "",
            "/static/images/a.png",
            "/static/images/b.png",
            "/static/images/b.png",
        ),
        content_markdown=md_with_psi,
    )

    uc = GetPostUseCase(repo=FakeRepo(post), renderer=IdentityRenderer())
    detail = uc.execute("demo")
    assert detail is not None
    assert "## Screenshots" in detail.content_html
    # Only one occurrence of each URL.
    assert detail.content_html.count("/static/images/a.png") == 1
    assert detail.content_html.count("/static/images/b.png") == 1

    # No PSI section but author provided Screenshots section: it should be retained.
    md_with_screens = "# Title\n\nIntro\n\n## Screenshots\n\n![x](/static/images/x.png)\n"
    post2 = MarkdownPost(
        slug="demo2",
        title="Demo2",
        date="2026-01-01 12:00",
        tags=("x",),
        blurb=None,
        one_liner=None,
        # Provide an explicit cover image so `GetPostUseCase` does *not* treat the
        # embedded screenshot image as the cover (the cover-strip is restricted to
        # the first 2 paragraphs).
        image="/static/images/cover.png",
        thumb_image=None,
        emoji=None,
        social_image=None,
        extra_images=(),
        content_markdown=md_with_screens,
    )
    uc2 = GetPostUseCase(repo=FakeRepo(post2), renderer=IdentityRenderer())
    detail2 = uc2.execute("demo2")
    assert detail2 is not None
    assert "## Screenshots" in detail2.content_html
    assert "/static/images/x.png" in detail2.content_html


def test_get_post_usecase_has_psi_but_no_screenshots_no_changes():
    """Covers the `has_psi` path where there are zero screenshot URLs and no embedded screenshots."""

    from app.usecases.get_post import GetPostUseCase

    class IdentityRenderer:
        def render(self, markdown_text: str) -> str:
            return markdown_text

    class FakeRepo:
        def __init__(self, post: MarkdownPost):
            self._post = post

        def list_posts(self):
            return (self._post,)

        def get_post(self, slug: str):
            return self._post if slug == self._post.slug else None

    md_with_psi_no_images = (
        "## Problem -> Solution -> Impact\n\n"
        "Text only.\n\n"
        "## Next\n\n"
        "Still text.\n"
    )

    post = MarkdownPost(
        slug="psi-no-images",
        title="PSI No Images",
        date="2026-01-01 12:00",
        tags=("x",),
        blurb=None,
        one_liner=None,
        image=None,
        thumb_image=None,
        emoji=None,
        social_image=None,
        extra_images=(),
        content_markdown=md_with_psi_no_images,
    )

    uc = GetPostUseCase(repo=FakeRepo(post), renderer=IdentityRenderer())
    detail = uc.execute("psi-no-images")
    assert detail is not None
    # No screenshot content injected.
    assert "## Screenshots" not in detail.content_html
    assert detail.content_html.strip().startswith("## Problem")


def test_strip_image_paragraph_tail_branch_covered():
    from app.usecases.list_posts import _strip_image_paragraph

    md = "Para\n\n![Alt](/static/images/cover.png)\n"
    out = _strip_image_paragraph(md, "/static/images/cover.png", tail=1)
    assert "cover.png" not in out


def test_excluded_slugs_blog_query_empty_set_branch_covered():
    """Covers the `_excluded_slugs_for_query()` branch where the CSV is empty."""

    class FakeBlog:
        def list_posts(self):
            return ()

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?q=cat:Blog&exclude_blog=0")
    assert resp.status_code == 200


def test_is_blog_post_by_cat_covers_branches():
    from app.http.routers.html import _is_blog_post_by_cat

    assert _is_blog_post_by_cat([]) is False
    assert _is_blog_post_by_cat(["x"]) is False
    assert _is_blog_post_by_cat(["cat:Blog"]) is True
    assert _is_blog_post_by_cat(["cat:blog"]) is True
    assert _is_blog_post_by_cat(["CAT:BLOG"]) is True


def test_homepage_leadership_missing_posts_is_tolerated(monkeypatch):
    """Leadership section is derived from lead slugs; missing slugs must not break the homepage."""

    posts = (
        # Intentionally provide no lead posts.
        _mk_summary(
            slug="hello-crank",
            title="Hello Crank",
            date="2026-01-17 11:00",
            tags=("post",),
        ),
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert "Hello Crank" in resp.text


def test_posts_index_category_title_empty_is_tolerated(monkeypatch):
    """Covers the `cat_text == ''` branch when computing category SEO titles."""

    posts = (
        _mk_summary(
            slug="lead1",
            title="Leadership One",
            date="2026-02-07 10:10",
            tags=("cat:Leadership",),
        ),
    )

    class FakeBlog:
        def list_posts(self):
            return posts

        def get_post(self, slug: str):
            return None

    from app.http.deps import get_blog_service
    from app.http.routers import html as html_router

    # Force `cat_display` to become empty after `.strip()` so the code exercises
    # the `if cat_text:` false branch.
    monkeypatch.setattr(html_router, "_category_label_for_query", lambda *a, **k: " ")

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
    client = TestClient(app)

    resp = client.get("/posts?q=cat:Leadership")
    assert resp.status_code == 200


def test_get_post_includes_author_screenshots_section_when_has_psi(monkeypatch):
    """Covers the branch that re-attaches author-provided Screenshots under PSI."""

    from app.usecases.get_post import GetPostUseCase

    md = (
        "---\n"
        "title: 'Demo'\n"
        "date: '2026-02-01'\n"
        "tags: ['x']\n"
        "---\n\n"
        "# Demo\n\n"
        "## Problem -> Solution -> Impact\n\n"
        "Some content.\n\n"
        "## Screenshots\n\n"
        "![shot](/static/images/me.jpg)\n\n"
        "More screenshots text.\n\n"
        "## Next\n\n"
        "Tail.\n"
    )

    post = MarkdownPost(
        slug="demo",
        title="Demo",
        date="2026-02-01 12:00",
        tags=("x",),
        blurb=None,
        one_liner=None,
        image=None,
        thumb_image=None,
        extra_images=(),
        content_markdown=md,
        emoji=None,
        social_image=None,
    )

    class FakeRepo:
        def get_post(self, slug: str):
            assert slug == "demo"
            return post

    class IdentityRenderer:
        def render(self, markdown_text: str) -> str:
            # For coverage tests we can treat markdown as the final output.
            return markdown_text

    uc = GetPostUseCase(repo=FakeRepo(), renderer=IdentityRenderer())
    detail = uc.execute("demo")
    assert detail is not None

    # The section should still exist after processing.
    assert "## Screenshots" in detail.content_html
    assert "More screenshots text." in detail.content_html

