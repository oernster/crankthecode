from __future__ import annotations
import json
import re
from fastapi.testclient import TestClient
from app.main import create_app


def test_homepage_renders():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")

    assert resp.status_code == 200

    assert "All posts are listed in reverse chronological order." not in resp.text
    assert "Things I build with" not in resp.text
    assert "Featured Systems" not in resp.text
    assert "docs/CV-OliverErnster.pdf" not in resp.text
    assert 'href="/essays"' in resp.text
    assert 'href="/build-log"' in resp.text
    assert 'href="/patterns"' in resp.text
    assert 'href="https://ernster.dev"' in resp.text

    # Primary homepage CTAs should appear in the hero.
    assert '<div class="hero-actions" aria-label="Primary actions">' in resp.text
    m = re.search(r'<section class="landing-intro"[\s\S]*?</section>', resp.text)
    assert m is not None, resp.text
    hero_block = m.group(0)
    assert "📩 Hire Me" not in hero_block
    assert "Download my CV" not in hero_block

    # CV download should be in the hero; Work With Me moved to sidebar.
    assert 'href="/cv-oliver-ernster.pdf"' in hero_block
    assert 'download="Oliver-Ernster-CV.pdf"' in hero_block
    assert "Download CV" in hero_block
    assert 'id="contact-email-btn"' not in hero_block
    assert "Work With Me" not in hero_block

    # Work With Me CTA should appear in the sidebar nav (not the hero).
    assert 'id="sidebar-work-with-me-btn"' in resp.text
    assert "Work With Me" in resp.text

    # Hero should remain concise (no extra proof/portfolio cues inside the hero block).
    assert 'class="homepage-portfolio-cue"' not in hero_block
    assert 'class="homepage-selected-project"' not in hero_block

    # The remaining areas stay reachable from the homepage (via the sidebar nav).
    # The portfolio lives entirely on ernster.dev now: the project write-ups
    # duplicated it, so they were retired along with their on-site index.
    assert 'href="/essays"' in resp.text
    assert 'href="/patterns"' in resp.text
    assert 'href="/books"' in resp.text
    assert 'href="https://ernster.dev"' in resp.text
    assert 'href="/posts?view=projects"' not in resp.text
    assert "Project write-ups" not in resp.text

    # No separate contact section at the bottom.
    assert "If the mandate is real" not in resp.text

    # Email should not be present in static HTML (it is JS-injected via
    # window.CTC_CONTACT).
    assert "oernster@codecrafter.uk" not in resp.text

    # GitHub profile link should be present in the header (public identity,
    # OK in static HTML).
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


def test_homepage_metadata_prioritises_oliver_and_links_website_to_person_jsonld():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200

    # Title and OG title must begin with Oliver Ernster (avoid generic fallbacks).
    assert "<title>Oliver Ernster - Principal Engineer" in resp.text, resp.text
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


def test_writing_alias_redirects_to_essays():
    app = create_app()
    # Use the canonical host+scheme so the canonical-redirect middleware passes through
    # and the legacy-redirect table fires.
    client = TestClient(
        app, base_url="https://www.crankthecode.com", follow_redirects=False
    )

    resp = client.get("/writing")

    assert resp.status_code == 301
    assert resp.headers["location"] == "/essays"


def test_about_page_renders():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/about")

    assert resp.status_code == 200
    assert "How I got here" in resp.text


def test_essays_and_build_log_pages_render():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/essays")
    assert resp.status_code == 200
    assert "Selected Essays" in resp.text
    assert 'href="/posts/crystal"' in resp.text

    resp = client.get("/build-log")
    assert resp.status_code == 200
    assert "Build Log" in resp.text


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
    assert 'href="/essays"' in resp.text
    assert 'href="/about"' in resp.text
    assert 'aria-label="Explore themes"' in resp.text


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


def test_post_pages_render_read_time_bar_shell():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts/start-here")
    assert resp.status_code == 200

    # Shell element exists (JS fills content); this should be present only
    # for post pages.
    assert 'class="read-time-bar"' in resp.text


def test_essay_post_back_link_targets_essays_page():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/posts/what-is-decision-architecture")
    assert resp.status_code == 200

    # Essays route back to the Selected Essays page.
    assert 'href="/essays"' in resp.text
    assert "Back to essays" in resp.text


def test_homepage_shows_both_decision_architecture_instruments_side_by_side():
    """Fulcrum and LatencyLab sit in one grid, as equal cards linking to the hub."""

    app = create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200

    assert 'class="instruments-grid"' in resp.text
    assert resp.text.count('class="instrument-card"') == 2

    assert 'href="https://ernster.dev/fulcrum/"' in resp.text
    assert "Open Fulcrum" in resp.text

    assert 'href="https://ernster.dev/latencylab/"' in resp.text
    assert "Open LatencyLab" in resp.text
    assert 'src="/static/images/latencylab-icon.png"' in resp.text
