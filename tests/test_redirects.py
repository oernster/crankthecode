from __future__ import annotations

from fastapi.testclient import TestClient

from app.http.redirects import REMOVED_POST_SLUGS, resolve_redirect
from app.main import create_app


def test_every_removed_post_slug_redirects_to_books():
    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    for slug in REMOVED_POST_SLUGS:
        resp = client.get(f"/posts/{slug}", follow_redirects=False)
        assert resp.status_code == 301, slug
        assert resp.headers.get("location") == "/books", slug


def test_legacy_posts_views_redirect_but_live_filters_fall_through():
    # Legacy views.
    assert resolve_redirect("/posts", {"view": "writing"}) == "/essays"
    assert resolve_redirect("/posts", {"view": "writing", "cat": "Blog"}) == (
        "/build-log"
    )

    # Live filters keep working on /posts.
    assert resolve_redirect("/posts", {"view": "archive"}) is None
    assert resolve_redirect("/posts", {"view": "writing", "q": "python"}) is None
    assert resolve_redirect("/posts", {"view": "writing", "layer": "architecture"}) is (
        None
    )
    assert resolve_redirect("/posts", {"view": "writing", "cat": "Governance"}) is None
    assert resolve_redirect("/posts", {}) is None

    # Non-table paths fall through.
    assert resolve_redirect("/books", {}) is None
    assert resolve_redirect("", {}) is None

    # Trailing slashes normalise onto the table.
    assert resolve_redirect("/decision-architecture/", {}) == "/essays"
