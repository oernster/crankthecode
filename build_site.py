"""Render the site to static files that GitHub Pages can serve.

The FastAPI application stays the only place a page is defined. This script asks
it for every URL in-process through Starlette's test client, then writes each
answer to disk. No template is rendered anywhere else, so the static site cannot
drift from the application.

What a static host cannot do is answered here instead:

- A page is written as `<path>.html`, which is served at `<path>` itself, so
  every URL keeps its current form with no trailing-slash redirect. That matters
  beyond tidiness: `static/search.js` recognises the posts index by the exact
  pathname `/posts`.
- A 301 becomes a small page that sends the browser on, since Pages cannot
  answer with a redirect.
- Anything that is not HTML (the feeds, the sitemap, the posts JSON the search
  box reads) is written at its exact path.
- Every internal link on every page must land on a written file; otherwise the
  build fails naming the page and the link.

    python build_site.py            # build into site/
    python build_site.py --serve    # build, then serve site/ on localhost
"""

from __future__ import annotations

import argparse
import functools
import html
import http.server
import os
import pathlib
import re
import shutil
import subprocess
import sys
from collections import deque
from urllib.parse import urljoin, urlsplit

REPO_ROOT = pathlib.Path(__file__).resolve().parent
DEFAULT_OUT = REPO_ROOT / "site"
DEFAULT_PORT = 8000
LOCAL_HOST = "127.0.0.1"

EXIT_OK = 0
EXIT_BROKEN_LINKS = 1

HTML_SUFFIX = ".html"
INDEX_FILE = "index.html"
NOT_FOUND_FILE = "404.html"
CNAME_FILE = "CNAME"

_LINK_ATTRIBUTE = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""")
_SITEMAP_LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")

REDIRECT_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
</head>
<body><p>This page has moved to <a href="{target}">{target}</a>.</p></body>
</html>
"""

NOT_FOUND_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found</title>
<meta name="robots" content="noindex">
</head>
<body><p>There is no page here. <a href="/">Go to the front page</a>.</p></body>
</html>
"""


def resolve(out: pathlib.Path, url_path: str) -> pathlib.Path | None:
    """The written file a URL path is served from; None when there is none.

    The order is the file itself, then `<path>.html`, then `<path>/index.html`,
    which is the order the local server below uses and the one the deploy's
    smoke check confirms on Pages.
    """
    relative = url_path.strip("/")
    if not relative:
        return out / INDEX_FILE if (out / INDEX_FILE).is_file() else None
    candidates = (
        out / relative,
        out / f"{relative}{HTML_SUFFIX}",
        out / relative / INDEX_FILE,
    )
    return next((path for path in candidates if path.is_file()), None)


def broken_links(out: pathlib.Path, links: dict[str, set[str]]) -> list[str]:
    """Every `page -> link` pair whose link lands on no written file."""
    return sorted(
        f"{page} -> {link}"
        for page, targets in links.items()
        for link in targets
        if resolve(out, link) is None
    )


def output_path(out: pathlib.Path, url_path: str, is_html: bool) -> pathlib.Path:
    """Where a response for `url_path` is written."""
    relative = url_path.strip("/")
    if not relative:
        return out / INDEX_FILE
    if is_html and not relative.endswith(HTML_SUFFIX):
        return out / f"{relative}{HTML_SUFFIX}"
    return out / relative


def _internal_path(link: str, page: str, site_url: str) -> str | None:
    """The path of `link` when it points into this site; None otherwise."""
    parts = urlsplit(urljoin(urljoin(site_url, page), link))
    if parts.scheme not in ("http", "https"):
        return None
    if parts.netloc != urlsplit(site_url).netloc:
        return None
    return parts.path or "/"


def route_paths(routes, prefix: str = "") -> set[str]:
    """Every GET route without a path parameter, however FastAPI holds them.

    FastAPI up to 0.128 flattened each included router into `app.routes`; by
    0.143 an included router stays nested, carrying its prefix in an
    `include_context`. CI installs the newest release, so both shapes are
    walked. Reading only the flat one cost the CI build its sitemap, its feeds
    and every redirect.
    """
    from fastapi.routing import APIRoute

    found: set[str] = set()
    for route in routes:
        included = getattr(route, "include_context", None)
        if included is not None:
            nested = included.included_router.routes
            found |= route_paths(nested, prefix + included.prefix)
        elif isinstance(route, APIRoute) and "GET" in route.methods:
            if "{" not in route.path:
                found.add(prefix + route.path)
    return found


def _seed_paths(app) -> set[str]:
    """Every route without a path parameter, every post and the legacy URLs.

    Most pages are reached by following links from these. Some posts are
    deliberately linked from nowhere (about-me) yet the search box still offers
    them. The legacy URLs exist only for old inbound links. Both are therefore
    named outright.
    """
    from app.http.deps import get_blog_service
    from app.http.redirects import REDIRECT_TABLE
    from app.http.routers import posts as posts_router

    routes = route_paths(app.routes)
    slugs = (
        {post.slug for post in get_blog_service().list_posts()}
        | posts_router._LEGACY_POST_REDIRECTS.keys()
        | posts_router._LEGACY_POST_ALIASES.keys()
    )
    return routes | REDIRECT_TABLE.keys() | {f"/posts/{s}" for s in slugs}


def _copy_static_mounts(app, out: pathlib.Path) -> None:
    """Copy each directory the application mounts, exactly as it mounts it."""
    from starlette.routing import Mount
    from starlette.staticfiles import StaticFiles

    for route in app.routes:
        if isinstance(route, Mount) and isinstance(route.app, StaticFiles):
            target = out / route.path.strip("/")
            shutil.copytree(route.app.directory, target, dirs_exist_ok=True)


def _crawl(client, app, out: pathlib.Path, site_url: str) -> dict[str, set[str]]:
    """Write every reachable URL; answer the internal links found on each page."""
    links: dict[str, set[str]] = {}
    queue = deque(sorted(_seed_paths(app)))
    seen: set[str] = set()
    while queue:
        path = queue.popleft()
        if path in seen:
            continue
        seen.add(path)
        response = client.get(path, follow_redirects=False)
        if response.is_redirect:
            target = urljoin(site_url, response.headers["location"])
            page = REDIRECT_PAGE.format(target=html.escape(target, quote=True))
            _write(output_path(out, path, is_html=True), page.encode())
            continue
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        is_html = "text/html" in content_type
        _write(output_path(out, path, is_html=is_html), response.content)
        if is_html:
            found = _LINK_ATTRIBUTE.findall(response.text)
        elif "xml" in content_type:
            found = _SITEMAP_LOC.findall(response.text)
        else:
            continue
        internal = {_internal_path(link, path, site_url) for link in found}
        internal.discard(None)
        if is_html:
            links[path] = internal
        queue.extend(link for link in internal if not link.startswith("/static/"))
    return links


def _write(path: pathlib.Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def refuse_unsafe_out(out: pathlib.Path) -> None:
    """Stop when `out` holds the repository, since the build clears it first."""
    if out.resolve() in (REPO_ROOT, *REPO_ROOT.parents):
        raise SystemExit(f"Refusing to clear {out}: it holds the repository.")


def build(out: pathlib.Path) -> int:
    """Build the site into `out`; answer the exit code."""
    refuse_unsafe_out(out)

    # The app resolves templates/, static/ and static_dist/ against the working
    # directory, so the build runs from the repository root wherever it starts.
    os.chdir(REPO_ROOT)
    os.environ.setdefault("CTC_USE_STATIC_DIST", "1")
    subprocess.run([sys.executable, "-m", "app.assets.build_static"], check=True)

    from fastapi.testclient import TestClient

    from app.http.seo import get_site_url
    from app.main import create_app

    site_url = get_site_url()
    app = create_app()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # Requests carry the production origin, so the canonical-host middleware
    # lets them through and every absolute URL a page builds is the real one.
    with TestClient(app, base_url=site_url.rstrip("/")) as client:
        links = _crawl(client, app, out, site_url)
    _copy_static_mounts(app, out)
    _write(out / NOT_FOUND_FILE, NOT_FOUND_PAGE.encode())
    _write(out / CNAME_FILE, f"{urlsplit(site_url).hostname}\n".encode())

    broken = broken_links(out, links)
    if broken:
        print(f"{len(broken)} internal link(s) land on nothing:", file=sys.stderr)
        for line in broken:
            print(f"  {line}", file=sys.stderr)
        return EXIT_BROKEN_LINKS
    written = sum(1 for path in out.rglob("*") if path.is_file())
    print(f"Built {len(links)} pages ({written} files) into {out}")
    return EXIT_OK


class _SiteHandler(http.server.SimpleHTTPRequestHandler):
    """Serves the built site with the same path rules as `resolve`."""

    def translate_path(self, path: str) -> str:
        out = pathlib.Path(self.directory)
        found = resolve(out, urlsplit(path).path)
        return str(found) if found else super().translate_path(path)


def serve(out: pathlib.Path, port: int) -> None:
    handler = functools.partial(_SiteHandler, directory=str(out))
    with http.server.ThreadingHTTPServer((LOCAL_HOST, port), handler) as server:
        print(f"Serving {out} at http://{LOCAL_HOST}:{port}/ (Ctrl+C stops it)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=DEFAULT_OUT,
        help=f"output directory (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--serve", action="store_true", help="serve the build on localhost"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="port for --serve"
    )
    args = parser.parse_args(argv)
    out = args.out.resolve()
    code = build(out)
    if code == EXIT_OK and args.serve:
        serve(out, args.port)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
