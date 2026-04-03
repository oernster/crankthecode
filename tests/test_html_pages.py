from __future__ import annotations

import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app
from app.domain.books_catalogue import BookCatalogueEntry


def test_homepage_renders():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")

    assert resp.status_code == 200

    assert "All posts are listed in reverse chronological order." not in resp.text
    assert "Things I build with" not in resp.text
    assert "Featured Systems" not in resp.text
    assert "docs/CV-Oliver.pdf" in resp.text
    assert 'href="/decision-architecture"' in resp.text
    assert 'href="/patterns"' in resp.text
    assert "🗺️ Start Here" in resp.text
    assert 'href="/posts/start-here"' in resp.text

    # Featured essay (single CTA) should appear between hero and gateways.
    assert 'aria-label="Featured essay"' in resp.text
    assert 'href="/posts/OODAIntro"' in resp.text
    assert "What is Decision Architecture?" in resp.text
    assert "🧩" in resp.text

    # Primary homepage CTAs must not appear in the hero (manifesto-first reading).
    assert '<div class="hero-actions" aria-label="Primary actions">' in resp.text
    m = re.search(r'<section class="landing-intro"[\s\S]*?</section>', resp.text)
    assert m is not None, resp.text
    hero_block = m.group(0)
    assert "📩 Hire Me" not in hero_block
    assert "Download my CV" not in hero_block

    # Minimal proof-of-execution cue should live inside the homepage intro.
    assert 'class="homepage-selected-project"' in hero_block
    assert "Selected project:" in hero_block
    assert 'href="/posts/narratex"' in hero_block
    assert "NarrateX</a> - local audiobook system." in hero_block

    # But the CTAs must appear in the contact section at the end.
    m = re.search(r'<section id="contact"[\s\S]*?</section>', resp.text)
    assert m is not None, resp.text
    contact_block = m.group(0)
    assert "Download my CV" in contact_block
    assert "📩 Hire Me" not in contact_block
    assert 'id="contact-email"' in contact_block

    # Email should not be present in static HTML (it is JS-injected via window.CTC_CONTACT).
    assert "oernster@codecrafter.uk" not in resp.text

    # GitHub profile link should be present in the header (public identity, OK in static HTML).
    assert 'href="https://github.com/oernster"' in resp.text
    assert 'aria-label="Oliver Ernster GitHub Profile"' in resp.text
    assert 'title="github.com/oernster"' in resp.text
    assert 'target="_blank"' in resp.text
    assert 'rel="noopener noreferrer me"' in resp.text

    # Contact pieces must not appear in clear text inside the bootstrap script.
    # (The site can still legitimately reference the GitHub username elsewhere.)
    m = re.search(
        r"window\.CTC_CONTACT\s*=\s*\(function\s*\(\)\s*\{[\s\S]*?\}\)\s*\(\)\s*;",
        resp.text,
    )
    assert m is not None, "CTC_CONTACT bootstrap script not found"
    contact_js = m.group(0)
    assert "oernster@codecrafter.uk" not in contact_js
    assert 'const user = "oernster"' not in contact_js
    assert 'const domain = "codecrafter"' not in contact_js
    assert 'const tld = "uk"' not in contact_js
    assert "atob(" in contact_js

    # Homepage should not show app/system button sections.
    assert "Engineering Experiments" not in resp.text
    assert 'aria-label="Tooling links"' not in resp.text


def test_homepage_featured_projects_uses_narratex_thumbnail_image_not_emoji():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200

    # Homepage no longer renders app/system project buttons.
    assert "/static/images/narratex-icon" not in resp.text


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
    monkeypatch.setenv("CTC_USE_STATIC_DIST", "1")
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


def test_docs_epub_is_not_served():
    """EPUBs are retained in-repo but should not be publicly downloadable via `/docs`."""

    app = create_app()
    client = TestClient(app)

    resp = client.get("/docs/Decision-Architecture.epub")
    assert resp.status_code == 404


def test_books_page_renders_and_links_to_amazon_uk():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/books")
    assert resp.status_code == 200

    assert "Books" in resp.text

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

    # Canonical Amazon UK links (no link switching)
    assert "https://www.amazon.co.uk/dp/B0GT4JNMGK" in resp.text
    assert "https://www.amazon.co.uk/dp/B0GT4CZ327" in resp.text
    assert "https://www.amazon.co.uk/dp/B0GT7D4P8G" in resp.text
    assert "https://www.amazon.co.uk/dp/B0GTDX7186" in resp.text

    # Hover/subtitle text should be present (consistent behaviour across cards).
    assert "A Positional Model of Organisational Change" in resp.text

    # Subtitles must be visible (not hover-only) and must match hover text.
    assert re.search(
        r'class="book-title">\s*Decision Architecture\s*</div>',
        resp.text,
    ), resp.text
    assert re.search(
        r'class="book-subtitle">\s*How technical organisations fail and recover\s*</div>',
        resp.text,
    ), resp.text

    assert re.search(
        r'class="book-title">\s*Decision Architecture: The Move Space\s*</div>',
        resp.text,
    ), resp.text
    assert re.search(
        r'class="book-subtitle">\s*A Positional Model of Organisational Change\s*</div>',
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
    # Author page should expose topic hubs for structural navigation.
    assert "Topics" in resp.text
    assert "decision-systems" in resp.text


def test_topics_pages_render():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/topics")
    assert resp.status_code == 200
    assert "Topics" in resp.text
    assert 'href="/topics/decision-systems"' in resp.text

    resp = client.get("/topics/decision-systems")
    assert resp.status_code == 200
    assert "Decision Systems" in resp.text


def test_about_author_alias_redirects_to_about():
    app = create_app()
    # Use localhost to bypass canonical-host middleware so we test the route handler.
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/about/oliver-ernster", follow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers.get("location") == "/about"


def test_start_here_includes_orientation_links():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts/start-here")
    assert resp.status_code == 200
    # Orientation / Explore navigation should no longer be injected into Start Here.
    assert 'aria-label="Orientation"' not in resp.text
    assert 'aria-label="Explore themes"' not in resp.text


def test_explore_page_renders_orientation_and_theme_links():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/explore")

    assert resp.status_code == 200
    assert 'aria-label="Orientation"' in resp.text
    assert 'href="/topics"' in resp.text
    assert 'href="/about"' in resp.text
    assert 'aria-label="Explore themes"' in resp.text
    assert 'href="/topics/decision-systems"' in resp.text


def test_help_redirects_to_explore():
    app = create_app()
    # Use localhost to bypass canonical-host middleware so we test the route handler.
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/help", follow_redirects=False)

    assert resp.status_code == 301
    assert resp.headers.get("location") == "/explore"


def test_unknown_post_returns_404_html():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts/definitely-not-a-real-post")

    assert resp.status_code == 404
    assert "Post Not Found" in resp.text
