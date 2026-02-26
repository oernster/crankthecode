from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.main import create_app


def test_homepage_renders():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")

    assert resp.status_code == 200
    assert "Featured Projects" in resp.text
    assert "docs/CV-Oliver.pdf" in resp.text
    assert "🗺️ Start Here" in resp.text
    assert 'href="/posts/start-here"' in resp.text


def test_homepage_metadata_prioritises_oliver_and_links_website_to_person_jsonld():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200

    # Title and OG title must begin with Oliver Ernster (avoid generic fallbacks).
    assert (
        "<title>Oliver Ernster - Senior Python Developer" in resp.text
    ), resp.text
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
    assert website.get("author") == {"@id": "https://www.crankthecode.com/#oliver-ernster"}


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

