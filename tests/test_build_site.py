"""The static build for GitHub Pages: its path rules, its link check, its output.

The path rules are what make a static host answer the same URLs the application
does, so they are pinned one by one. The link check is proved by planting a
broken link rather than trusted. The end-to-end test runs the real build in a
child process, because the build sets environment variables and changes
directory, neither of which may leak into the rest of the suite.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import build_site

SITE_HOST = "www.crankthecode.com"


def _touch(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_root_resolves_to_the_index(tmp_path: Path) -> None:
    _touch(tmp_path / "index.html")

    assert build_site.resolve(tmp_path, "/") == tmp_path / "index.html"


def test_a_page_is_served_from_its_html_file_before_a_directory(
    tmp_path: Path,
) -> None:
    # /posts must not become /posts/: search.js matches the exact pathname.
    _touch(tmp_path / "posts.html")
    _touch(tmp_path / "posts" / "index.html")

    assert build_site.resolve(tmp_path, "/posts") == tmp_path / "posts.html"


def test_an_exact_file_wins_over_its_html_twin(tmp_path: Path) -> None:
    _touch(tmp_path / "rss.xml")
    _touch(tmp_path / "rss.xml.html")

    assert build_site.resolve(tmp_path, "/rss.xml") == tmp_path / "rss.xml"


def test_a_directory_index_is_the_last_resort(tmp_path: Path) -> None:
    _touch(tmp_path / "static" / "index.html")

    assert build_site.resolve(tmp_path, "/static/") == (
        tmp_path / "static" / "index.html"
    )


def test_nothing_resolves_to_none(tmp_path: Path) -> None:
    assert build_site.resolve(tmp_path, "/") is None
    assert build_site.resolve(tmp_path, "/missing") is None


def test_html_is_written_beside_its_url_and_everything_else_at_it(
    tmp_path: Path,
) -> None:
    assert build_site.output_path(tmp_path, "/", True) == tmp_path / "index.html"
    assert build_site.output_path(tmp_path, "/posts/a", True) == (
        tmp_path / "posts" / "a.html"
    )
    assert build_site.output_path(tmp_path, "/api/posts", False) == (
        tmp_path / "api" / "posts"
    )


def test_the_link_check_names_a_planted_broken_link(tmp_path: Path) -> None:
    _touch(tmp_path / "index.html")
    _touch(tmp_path / "about.html")

    broken = build_site.broken_links(tmp_path, {"/": {"/about", "/gone"}})

    assert broken == ["/ -> /gone"]


def test_the_output_may_not_hold_the_repository(tmp_path: Path) -> None:
    # The guard is called directly, never through build(): were it ever to
    # regress, build() itself would clear the repository.
    for unsafe in (build_site.REPO_ROOT, build_site.REPO_ROOT.parent):
        with pytest.raises(SystemExit, match="Refusing"):
            build_site.refuse_unsafe_out(unsafe)

    build_site.refuse_unsafe_out(tmp_path / "site")


def test_the_real_build_writes_a_servable_site(tmp_path: Path) -> None:
    out = tmp_path / "site"
    result = subprocess.run(
        [sys.executable, str(build_site.REPO_ROOT / "build_site.py"), "--out", out],
        capture_output=True,
        text=True,
    )

    assert result.returncode == build_site.EXIT_OK, result.stderr
    for name in ("index.html", "posts.html", "404.html", "rss.xml", "sitemap.xml"):
        assert (out / name).is_file(), name
    assert (out / ".well-known" / "mmsp.json").is_file()
    assert (out / "CNAME").read_text(encoding="utf-8").strip() == SITE_HOST

    posts = json.loads((out / "api" / "posts").read_text(encoding="utf-8"))
    slugs = {post["slug"] for post in posts}
    assert slugs
    assert all((out / "posts" / f"{slug}.html").is_file() for slug in slugs)

    moved = (out / "help.html").read_text(encoding="utf-8")
    assert f"url=https://{SITE_HOST}/explore" in moved
    legacy = (out / "topics.html").read_text(encoding="utf-8")
    assert f"url=https://{SITE_HOST}/essays" in legacy
