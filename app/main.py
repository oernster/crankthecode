from __future__ import annotations

import os
from typing import Awaitable, Callable

from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from starlette.types import ASGIApp, Receive, Scope, Send

from app.assets.manifest import asset_url
from app.assets.staticfiles import CachingStaticFiles, FallbackStaticFiles
from app.http.routers.api import router as api_router
from app.http.routers.html import router as html_router
from app.http.routers.rss import router as rss_router
from app.http.routers.sitemap import router as sitemap_router


class _CachePolicyMiddleware:
    """Pure-ASGI cache-control middleware.

    Intercepts the ``http.response.start`` event and injects ``Cache-Control``
    headers at the ASGI protocol level — before any bytes reach the wire.

    This is more reliable than FastAPI's higher-level ``call_next`` middleware,
    which reconstructs the response object and can lose header mutations in
    some Starlette versions.

    Rules
    -----
    - ``text/html`` responses: ``no-store`` (never cache; forces fresh fetch on
      every navigation, even in CDN/proxy layers via ``CDN-Cache-Control`` and
      ``Surrogate-Control``).
    - ``application/rss+xml``, ``application/xml``, ``text/plain``: ``no-cache,
      must-revalidate`` (revalidate each time but allow conditional GETs).
    - Everything else: headers left as-is (static assets are handled by
      ``CachingStaticFiles`` with fingerprint-based immutable caching).
    """

    _HTML_HEADERS: list[tuple[bytes, bytes]] = [
        (b"cache-control", b"no-store"),
        (b"cdn-cache-control", b"no-store"),
        (b"surrogate-control", b"no-store"),
        (b"pragma", b"no-cache"),
        (b"expires", b"0"),
    ]

    _DYNAMIC_CC: bytes = b"no-cache, must-revalidate"

    _DYNAMIC_PREFIXES = (
        b"application/rss+xml",
        b"application/xml",
        b"text/plain",
    )

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_cache_policy(message: dict) -> None:
            if message["type"] == "http.response.start":
                headers: list[tuple[bytes, bytes]] = list(message.get("headers", []))
                content_type = b""
                for k, v in headers:
                    if k.lower() == b"content-type":
                        content_type = v.lower()
                        break

                if content_type.startswith(b"text/html"):
                    # Strip any existing Cache-Control / Pragma / Expires so our
                    # directives are the sole authority on this response.
                    _strip = {b"cache-control", b"cdn-cache-control", b"surrogate-control", b"pragma", b"expires"}
                    headers = [(k, v) for k, v in headers if k.lower() not in _strip]
                    headers.extend(self._HTML_HEADERS)
                    message = {**message, "headers": headers}

                elif any(content_type.startswith(p) for p in self._DYNAMIC_PREFIXES):
                    has_cc = any(k.lower() == b"cache-control" for k, _ in headers)
                    if not has_cc:
                        headers = list(headers) + [(b"cache-control", self._DYNAMIC_CC)]
                        message = {**message, "headers": headers}

            await send(message)

        await self.app(scope, receive, send_with_cache_policy)


def create_app() -> FastAPI:
    """FastAPI application factory."""

    fastapi_app = FastAPI()

    # Canonical host + scheme redirects (301)
    #
    # Goal:
    # - http://crankthecode.com        -> https://www.crankthecode.com
    # - http://www.crankthecode.com   -> https://www.crankthecode.com
    # - https://crankthecode.com      -> https://www.crankthecode.com
    #
    # Note:
    # - This only works when those hostnames route to this app.
    # - We bypass local dev hosts so `uvicorn` on 127.0.0.1/localhost behaves normally.
    CANONICAL_HOST = (os.getenv("CTC_CANONICAL_HOST") or "www.crankthecode.com").lower()

    @fastapi_app.middleware("http")
    async def enforce_canonical_host_and_scheme(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        hostname = (request.url.hostname or "").lower()
        if hostname in {"127.0.0.1", "localhost"}:
            return await call_next(request)

        forwarded_proto = (request.headers.get("x-forwarded-proto") or "").lower()
        scheme = forwarded_proto or request.url.scheme

        if hostname != CANONICAL_HOST or scheme != "https":
            path = request.url.path
            query = request.url.query
            target = f"https://{CANONICAL_HOST}{path}" + (f"?{query}" if query else "")
            return RedirectResponse(url=target, status_code=301)

        return await call_next(request)

    # Static and templates
    BASE_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = BASE_DIR.parent

    # Keep this parsing tolerant (Render/UI env vars can sometimes contain
    # whitespace depending on how they were entered).
    use_static_dist = (os.getenv("CTC_USE_STATIC_DIST") or "").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }

    static_dir = PROJECT_ROOT / ("static_dist" if use_static_dist else "static")

    # Log once at startup; useful to prove which directory is mounted in prod.
    print(">>> STATIC DIR:", static_dir)
    print(">>> ENV CTC_USE_STATIC_DIST:", os.getenv("CTC_USE_STATIC_DIST"))
    print(">>> ENV CTC_STATIC_MANIFEST_PATH:", os.getenv("CTC_STATIC_MANIFEST_PATH"))

    fastapi_app.mount(
        "/static",
        FallbackStaticFiles(directory=str(static_dir)),
        name="static",
    )

    configured_static_dist_dir = (os.getenv("CTC_STATIC_DIST_DIR") or "").strip()
    static_dist_dir = configured_static_dist_dir or "static_dist"

    # `docs/` is optional. Only mount if it exists, otherwise `/docs/...` should 404.
    if Path("docs").exists():
        fastapi_app.mount(
            "/docs",
            CachingStaticFiles(directory="docs"),
            name="docs",
        )

    @fastapi_app.get("/cv-oliver-ernster.pdf", include_in_schema=False)
    async def cv_pdf() -> FileResponse:
        """Serve the CV from a stable root URL.

        The source-of-truth lives in `static/` but production may serve from
        `static_dist/` when `CTC_USE_STATIC_DIST=1`.
        """

        static_dist_path = Path(static_dist_dir) / "CV-Oliver.pdf"
        static_src_path = Path("static") / "CV-Oliver.pdf"

        path = (
            static_dist_path
            if (use_static_dist and static_dist_path.exists())
            else static_src_path
        )
        return FileResponse(path)

    # Templates
    # - auto_reload + cache_size=0 ensures template edits are reflected without
    #   restarting the server
    #   (useful during local dev; acceptable overhead for this small site).
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=True,
        auto_reload=True,
        cache_size=0,
    )
    env.globals["asset_url"] = asset_url

    # Starlette's Jinja2Templates asserts XOR(directory, env). To avoid the
    # deprecation warning about passing extra env_options, we pass only `env`.
    fastapi_app.state.templates = Jinja2Templates(env=env)

    @fastapi_app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        resp = FileResponse("static/favicon.ico")
        # Favicons are often cached aggressively by browsers; force revalidation.
        resp.headers["Cache-Control"] = "no-cache, must-revalidate"
        return resp

    # Pure-ASGI cache middleware: intercepts http.response.start before any bytes
    # hit the wire — more reliable than call_next which can lose header mutations.
    fastapi_app.add_middleware(_CachePolicyMiddleware)

    fastapi_app.include_router(html_router)
    fastapi_app.include_router(api_router)
    fastapi_app.include_router(rss_router)
    fastapi_app.include_router(sitemap_router)

    return fastapi_app


app = create_app()
