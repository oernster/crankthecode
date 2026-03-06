from __future__ import annotations

import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def test_homepage_renders():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")

    assert resp.status_code == 200
    assert "Things I build with" not in resp.text
    assert "Featured Projects" in resp.text
    assert "docs/CV-Oliver.pdf" in resp.text
    assert 'href="/docs/Decision-Architecture.epub"' in resp.text
    assert "Download eBook" in resp.text
    assert "🗺️ Start Here" in resp.text
    assert 'href="/posts/start-here"' in resp.text


def test_html_cache_headers_are_no_store():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.headers.get("cache-control") == "no-cache, no-store, must-revalidate"
    assert resp.headers.get("pragma") == "no-cache"
    assert resp.headers.get("expires") == "0"


def test_favicon_is_not_cached_forever():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/favicon.ico")
    assert resp.status_code == 200
    # Browsers can be extremely sticky with favicons; force revalidation.
    assert resp.headers.get("cache-control") == "no-cache, must-revalidate"


def test_fingerprinted_static_assets_are_immutable_cached(monkeypatch):
    # Ensure the build output exists *before* app creation; `create_app()`
    # mounts `static_dist/` only if it exists.
    from app.assets.build_static import build_static_dist
    from app.assets.manifest import reset_asset_manifest_cache

    build_static_dist(
        static_src_dir=Path("static"),
        static_dist_dir=Path("static_dist"),
        manifest_path=Path("static_dist/manifest.json"),
        hash_len=10,
    )

    # Make the test hermetic even if the outer environment sets these.
    monkeypatch.setenv("CTC_STATIC_DIST_DIR", "static_dist")
    monkeypatch.setenv("CTC_STATIC_MANIFEST_PATH", "static_dist/manifest.json")
    reset_asset_manifest_cache()

    app = create_app()
    client = TestClient(app)

    html = client.get("/")
    assert html.status_code == 200

    # The homepage should reference fingerprinted CSS after build.
    m = re.search(r"/static/styles\.[0-9a-f]{8,}\.css", html.text)
    assert m is not None, html.text

    css_url = m.group(0)
    css = client.get(css_url)
    assert css.status_code == 200
    assert css.headers.get("cache-control") == "public, max-age=31536000, immutable"


def test_docs_epub_is_served():
    """The eBook should be directly downloadable like the CV (via `/docs`)."""

    app = create_app()
    client = TestClient(app)

    resp = client.get("/docs/Decision-Architecture.epub")
    assert resp.status_code == 200
    assert len(resp.content) > 0


def test_homepage_metadata_prioritises_oliver_and_links_website_to_person_jsonld():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200

    # Title and OG title must begin with Oliver Ernster (avoid generic fallbacks).
    assert "<title>Oliver Ernster - Senior Python Developer" in resp.text, resp.text
    assert (
        '<meta property="og:title" content="Oliver Ernster | Crank The Code">'
        in resp.text
    ), resp.text

    # Structured data should be a single script with @graph containing both
    # WebSite and Person and an author @id reference.
    marker = '<script type="application/ld+json">'
    assert resp.text.count(marker) == 1

    start = resp.text.index(marker) + len(marker)
    end = resp.text.index("</script>", start)
    payload = resp.text[start:end]

    data = json.loads(payload)
    assert data.get("@context") == "https://schema.org"
    graph = data.get("@graph")
    assert isinstance(graph, list)

    website = next((n for n in graph if n.get("@type") == "WebSite"), None)
    person = next((n for n in graph if n.get("@type") == "Person"), None)
    assert website is not None
    assert person is not None

    assert person.get("@id") == "https://www.crankthecode.com/#oliver-ernster"
    assert website.get("author") == {
        "@id": "https://www.crankthecode.com/#oliver-ernster"
    }


def test_posts_index_renders_and_supports_query_filter():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts")
    assert resp.status_code == 200
    assert "All posts" in resp.text

    filtered = client.get("/posts", params={"q": "python"})
    assert filtered.status_code == 200
    assert "All posts" in filtered.text


def test_about_page_renders():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/about")

    assert resp.status_code == 200
    assert "Things I build with" in resp.text


def test_help_page_renders_and_is_noindex_and_masks_email():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/help")

    assert resp.status_code == 200
    assert "You Clicked Help" in resp.text
    assert '<meta name="robots" content="noindex"' in resp.text
    assert "[enable JavaScript]" in resp.text
    # Ensure we don't include a literal mailto in the static HTML.
    assert "mailto:" not in resp.text


def test_unknown_post_returns_404_html():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts/definitely-not-a-real-post")

    assert resp.status_code == 404
    assert "Post Not Found" in resp.text
