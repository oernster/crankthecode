from __future__ import annotations

import json
import os
import runpy
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.assets.manifest import AssetManifest, get_asset_manifest, reset_asset_manifest_cache
from app.assets.staticfiles import CachingStaticFiles, FallbackStaticFiles


def test_build_static_hash_and_fingerprinted_name_helpers():
    import app.assets.build_static as build_static

    digest = build_static._hash_bytes(b"hello", length=10)
    assert len(digest) == 10
    assert all(c in "0123456789abcdef" for c in digest)

    assert build_static._fingerprinted_name("app.js", "deadbeef") == "app.deadbeef.js"
    assert build_static._fingerprinted_name("noext", "deadbeef") == "noext.deadbeef"


def test_build_static_dist_creates_manifest_and_fingerprinted_files(tmp_path: Path):
    import app.assets.build_static as build_static

    src = tmp_path / "static"
    dist = tmp_path / "static_dist"
    manifest = dist / "manifest.json"

    (src / "images").mkdir(parents=True)
    (src / "styles.css").write_text("body{color:red}", encoding="utf-8")
    (src / "images" / "me.jpg").write_bytes(b"jpgbytes")
    (src / ".gitkeep").write_text("", encoding="utf-8")
    (src / "images" / ".gitkeep").write_text("", encoding="utf-8")

    mapping = build_static.build_static_dist(
        static_src_dir=src,
        static_dist_dir=dist,
        manifest_path=manifest,
        hash_len=8,
    )

    assert mapping["styles.css"].startswith("styles.")
    assert mapping["styles.css"].endswith(".css")
    assert mapping["images/me.jpg"].startswith("images/me.")
    assert mapping["images/me.jpg"].endswith(".jpg")

    # Both original and fingerprinted copies exist.
    assert (dist / "styles.css").exists()
    assert (dist / mapping["styles.css"]).exists()
    assert (dist / "images" / "me.jpg").exists()
    assert (dist / mapping["images/me.jpg"]).exists()

    # Manifest JSON is written.
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["styles.css"] == mapping["styles.css"]


def test_build_static_dist_raises_when_src_missing(tmp_path: Path):
    import app.assets.build_static as build_static

    with pytest.raises(FileNotFoundError):
        build_static.build_static_dist(
            static_src_dir=tmp_path / "missing",
            static_dist_dir=tmp_path / "out",
            manifest_path=tmp_path / "out" / "manifest.json",
        )


def test_build_static_module_main_via_runpy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # Execute the module as `__main__` to cover the guarded entrypoint.
    src = tmp_path / "static"
    src.mkdir()
    (src / "styles.css").write_text("x", encoding="utf-8")

    dist = tmp_path / "static_dist"
    manifest = dist / "manifest.json"

    monkeypatch.setenv("CTC_STATIC_SRC_DIR", str(src))
    monkeypatch.setenv("CTC_STATIC_DIST_DIR", str(dist))
    monkeypatch.setenv("CTC_STATIC_MANIFEST_PATH", str(manifest))
    monkeypatch.setenv("CTC_STATIC_HASH_LEN", "8")

    # Ensure argparse uses defaults from env.
    monkeypatch.setattr(sys, "argv", ["build_static"], raising=True)

    # Avoid `runpy` warning by ensuring the module is not already imported.
    sys.modules.pop("app.assets.build_static", None)
    runpy.run_module("app.assets.build_static", run_name="__main__")

    assert manifest.exists()


def test_asset_manifest_load_handles_missing_and_invalid(tmp_path: Path):
    missing = AssetManifest.load(tmp_path / "nope.json")
    assert missing.mapping == {}

    invalid = tmp_path / "invalid.json"
    invalid.write_text("{not:json}", encoding="utf-8")
    assert AssetManifest.load(invalid).mapping == {}

    nondict = tmp_path / "nondict.json"
    nondict.write_text("[]", encoding="utf-8")
    assert AssetManifest.load(nondict).mapping == {}

    mixed = tmp_path / "mixed.json"
    # JSON coerces non-string keys to strings. Ensure we still filter out non-string values.
    mixed.write_text(json.dumps({"ok": "x.y.js", "1": "no", "bad": 2}), encoding="utf-8")
    man = AssetManifest.load(mixed)
    assert man.mapping == {"ok": "x.y.js", "1": "no"}


def test_asset_manifest_resolution_and_rewriting():
    man = AssetManifest(mapping={
        "styles.css": "styles.aaaaaaaa.css",
        "images/me.jpg": "images/me.bbbbbbbb.jpg",
    })

    assert man.static_url("styles.css") == "/static/styles.aaaaaaaa.css"
    assert man.resolve_url_or_path("https://example.com/x") == "https://example.com/x"
    assert man.resolve_url_or_path("/not-static/x") == "/not-static/x"
    assert man.resolve_url_or_path("/static/images/me.jpg") == "/static/images/me.bbbbbbbb.jpg"

    html = (
        '<img src="/static/images/me.jpg">'
        '<a href="/static/styles.css">x</a>'
        "<div style=\"background:url(/static/images/me.jpg)\"></div>"
    )
    out = man.rewrite_html_static_urls(html)
    assert "/static/images/me.bbbbbbbb.jpg" in out
    assert "/static/styles.aaaaaaaa.css" in out

    assert man.rewrite_html_static_urls("") == ""
    assert AssetManifest.is_fingerprinted_path("styles.1234abcd.css")
    assert not AssetManifest.is_fingerprinted_path("styles.css")


def test_asset_manifest_cache_reset(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"styles.css": "styles.11111111.css"}), encoding="utf-8")
    monkeypatch.setenv("CTC_STATIC_MANIFEST_PATH", str(path))

    reset_asset_manifest_cache()
    assert get_asset_manifest().static_url("styles.css") == "/static/styles.11111111.css"

    # Update manifest; cached value should not change until reset.
    path.write_text(json.dumps({"styles.css": "styles.22222222.css"}), encoding="utf-8")
    assert get_asset_manifest().static_url("styles.css") == "/static/styles.11111111.css"

    reset_asset_manifest_cache()
    assert get_asset_manifest().static_url("styles.css") == "/static/styles.22222222.css"


def test_caching_staticfiles_cache_headers(tmp_path: Path):
    static_dir = tmp_path / "static_dist"
    static_dir.mkdir()
    (static_dir / "app.1234abcd.js").write_text("console.log(1)", encoding="utf-8")
    (static_dir / "app.js").write_text("console.log(2)", encoding="utf-8")

    app = FastAPI()
    app.mount("/static", CachingStaticFiles(directory=str(static_dir)), name="static")
    client = TestClient(app)

    fp = client.get("/static/app.1234abcd.js")
    assert fp.status_code == 200
    assert fp.headers.get("cache-control") == "public, max-age=31536000, immutable"

    plain = client.get("/static/app.js")
    assert plain.status_code == 200
    assert plain.headers.get("cache-control") == "no-cache, must-revalidate"

    missing = client.get("/static/missing.js")
    assert missing.status_code == 404

    # Conditional request should yield 304, exercising the non-200 early return.
    lm = fp.headers.get("last-modified")
    if lm:
        not_modified = client.get("/static/app.1234abcd.js", headers={"if-modified-since": lm})
        assert not_modified.status_code == 304


def test_fallback_staticfiles_serves_from_fallback_on_404(tmp_path: Path):
    primary = tmp_path / "static_dist"
    fallback = tmp_path / "static"
    primary.mkdir()
    fallback.mkdir()

    # Only exists in fallback.
    (fallback / "only-fallback.txt").write_text("ok", encoding="utf-8")

    app = FastAPI()
    app.mount(
        "/static",
        FallbackStaticFiles(directory=str(primary), fallback_directory=str(fallback)),
        name="static",
    )
    client = TestClient(app)

    resp = client.get("/static/only-fallback.txt")
    assert resp.status_code == 200
    assert resp.text == "ok"


def test_fallback_staticfiles_propagates_404_when_no_fallback(tmp_path: Path):
    primary = tmp_path / "static_dist"
    primary.mkdir()

    app = FastAPI()
    app.mount(
        "/static",
        FallbackStaticFiles(directory=str(primary), fallback_directory=None),
        name="static",
    )
    client = TestClient(app)

    # Missing in primary and no fallback -> 404 must propagate.
    resp = client.get("/static/does-not-exist.txt")
    assert resp.status_code == 404


def test_fallback_staticfiles_uses_fallback_when_primary_returns_404_response(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    """Cover the non-exception 404 path.

    Starlette can raise for 404s, but our wrapper also handles a plain 404 Response
    defensively.
    """

    async def fake_get_response(self, path: str, scope):
        from starlette.responses import PlainTextResponse

        # Primary (FallbackStaticFiles instance): return a 404 Response.
        if isinstance(self, FallbackStaticFiles):
            return PlainTextResponse("missing", status_code=404)

        # Fallback (CachingStaticFiles instance): return 200.
        return PlainTextResponse("ok", status_code=200)

    monkeypatch.setattr(CachingStaticFiles, "get_response", fake_get_response)

    primary = tmp_path / "static_dist"
    fallback = tmp_path / "static"
    primary.mkdir()
    fallback.mkdir()

    app = FastAPI()
    app.mount(
        "/static",
        FallbackStaticFiles(directory=str(primary), fallback_directory=str(fallback)),
        name="static",
    )
    client = TestClient(app)

    resp = client.get("/static/anything.txt")
    assert resp.status_code == 200
    assert resp.text == "ok"

