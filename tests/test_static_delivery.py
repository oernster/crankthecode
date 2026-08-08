"""How static assets, the CV and the docs directory are served and cached."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def test_html_cache_headers_are_no_store():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    # Pure-ASGI middleware sets no-store at the protocol level: stronger than
    # call_next which can lose header mutations in some Starlette versions.
    assert resp.headers.get("cache-control") == "no-store"
    assert resp.headers.get("cdn-cache-control") == "no-store"
    assert resp.headers.get("surrogate-control") == "no-store"
    assert resp.headers.get("pragma") == "no-cache"
    assert resp.headers.get("expires") == "0"


def test_favicon_is_not_cached_forever():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/favicon.ico")
    assert resp.status_code == 200
    # Browsers can be extremely sticky with favicons; force revalidation.
    assert resp.headers.get("cache-control") == "no-cache, must-revalidate"


def test_cv_pdf_is_served_from_stable_root_path():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/cv-oliver-ernster.pdf")
    assert resp.status_code == 200

    content_type = (resp.headers.get("content-type") or "").lower()
    assert "pdf" in content_type
    assert resp.content.startswith(b"%PDF")


def test_cv_pdf_prefers_static_dist_when_enabled(tmp_path: Path, monkeypatch):
    dist = tmp_path / "static_dist"
    dist.mkdir(parents=True, exist_ok=True)

    # Ensure we can distinguish which file is served.
    cv_bytes = b"%PDF-1.7\n% test static_dist\n"
    (dist / "CV-OliverErnster.pdf").write_bytes(cv_bytes)

    monkeypatch.setenv("CTC_USE_STATIC_DIST", "1")
    monkeypatch.setenv("CTC_STATIC_DIST_DIR", str(dist))

    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/cv-oliver-ernster.pdf")
    assert resp.status_code == 200
    assert resp.content == cv_bytes


def test_app_starts_when_the_static_build_has_not_run(tmp_path: Path, monkeypatch):
    """A fresh checkout has no `static_dist/`, and the app must still serve.

    `static_dist/` is a build output and is gitignored, so on a clean clone it
    does not exist until the build has run. Mounting a missing directory raises
    at startup, which took CI down with a RuntimeError while passing locally
    purely because a built copy happened to be lying around. The app now falls
    back to the unfingerprinted sources.
    """
    missing = tmp_path / "never_built"
    assert not missing.exists()

    monkeypatch.setenv("CTC_USE_STATIC_DIST", "1")
    monkeypatch.setenv("CTC_STATIC_DIST_DIR", str(missing))

    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    # It serves, and it serves the plain sources rather than 500ing.
    resp = client.get("/static/styles.css")
    assert resp.status_code == 200


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

    # And fingerprinted JS assets referenced from the base template.
    for name in ("search", "scroll-top", "copy-code"):
        assert re.search(
            rf"/static/{re.escape(name)}\.[0-9a-f]{{8,}}\.js",
            html.text,
        ), html.text

    # Read-time is only included for some pages; assert it on a post detail page.
    post = client.get("/posts/start-here")
    assert post.status_code == 200
    assert re.search(r"/static/read-time\.[0-9a-f]{8,}\.js", post.text), post.text

    css_url = m.group(0)
    css = client.get(css_url)
    assert css.status_code == 200
    assert css.headers.get("cache-control") == "public, max-age=31536000, immutable"


def test_docs_epub_is_not_served():
    """EPUBs are retained in-repo but must not be downloadable via `/docs`."""

    app = create_app()
    client = TestClient(app)

    resp = client.get("/docs/Decision-Architecture.epub")
    assert resp.status_code == 404


def test_docs_directory_can_be_present_without_exposing_epub_downloads():
    """Cover the branch where `docs/` exists and is mounted.

    This should still 404 for EPUBs.
    """

    import shutil

    docs_dir = Path("docs")
    pre_existing = docs_dir.exists()

    if not pre_existing:
        docs_dir.mkdir(parents=True, exist_ok=True)

    try:
        app = create_app()
        client = TestClient(app, base_url="http://localhost")

        resp = client.get("/docs/Decision-Architecture.epub")
        assert resp.status_code == 404
    finally:
        if not pre_existing:
            shutil.rmtree(docs_dir)
