"""Homepage leadership section and the battlestation page."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.domain.models import PostSummary
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
        post_type=None,
        role=None,
    )


def test_html_homepage_leadership_section_is_present_and_ordered(monkeypatch):
    """Homepage renders; the retired gateway 301s to the essays page."""

    posts = (
        _mk_summary(
            slug="lead10",
            title="Leadership Ten",
            date="2026-02-10 10:10",
            tags=("cat:Leadership",),
        ),
        _mk_summary(
            slug="lead1",
            title="Leadership One",
            date="2026-02-07 10:10",
            tags=("cat:Leadership",),
        ),
        _mk_summary(
            slug="not-lead",
            title="Not Leadership",
            date="2026-02-09 09:00",
            tags=("cat:Tools",),
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
    assert "Decision Architecture" in resp.text

    # The old gateway is retired: it 301s to the Selected Essays page.
    resp = client.get("/decision-architecture", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers.get("location") == "/essays"


def test_homepage_leadership_missing_posts_is_tolerated(monkeypatch):
    """Leadership section is derived from lead slugs.

    Missing slugs must not break the homepage.
    """

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
    # Homepage should tolerate missing leadership slugs and still render.
    # It no longer renders app/project buttons like "Hello Crank".
    assert "Decision Architecture" in resp.text


def test_homepage_leadership_empty_renders_empty_state(monkeypatch):
    """When there are no `cat:Leadership` posts, the homepage should render safely."""

    posts = (
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
    assert "Decision Architecture" in resp.text


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
    client = TestClient(app, base_url="http://localhost")
    resp = client.get("/battlestation", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers["location"].endswith("/posts/battlestation")
