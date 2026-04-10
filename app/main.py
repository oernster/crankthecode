from __future__ import annotations

import os
from typing import Awaitable, Callable

from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

from app.assets.manifest import asset_url
from app.assets.staticfiles import CachingStaticFiles, FallbackStaticFiles
from app.http.routers.api import router as api_router
from app.http.routers.html import router as html_router
from app.http.routers.rss import router as rss_router
from app.http.routers.sitemap import router as sitemap_router


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
    CANONICAL_HOST = "www.crankthecode.com"

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

    @fastapi_app.middleware("http")
    async def cache_policy_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        resp = await call_next(request)

        # Apply cache policy based on response content type.
        content_type = (resp.headers.get("content-type") or "").lower()

        if content_type.startswith("text/html"):
            resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            resp.headers["Pragma"] = "no-cache"
            resp.headers["Expires"] = "0"
            return resp

        # Dynamic text endpoints (RSS, sitemap, robots) must be revalidated.
        if (
            content_type.startswith("application/rss+xml")
            or content_type.startswith("application/xml")
            or content_type.startswith("text/plain")
        ):
            resp.headers.setdefault("Cache-Control", "no-cache, must-revalidate")

        return resp

    # Static and templates
    #
    # We need local dev *and* production to be reliable.
    #
    # - Local dev: default to serving from `static/` (source of truth).
    #   Rationale: `static_dist/` is build output and can be stale or partially
    #   generated locally, which can cause wrong icons / broken images.
    #
    # - Production (Render): explicitly opt into `static_dist/` via
    #   `CTC_USE_STATIC_DIST=1`, so fingerprinted assets are served and cached
    #   immutably.
    #
    # When serving from `static_dist/`, we still fall back to `static/` for
    # missing files (useful during deploy transitions).
    def _truthy_env(name: str) -> bool:
        return (os.getenv(name) or "").strip().lower() in {
            "1",
            "true",
            "yes",
            "y",
            "on",
        }

    use_static_dist = _truthy_env("CTC_USE_STATIC_DIST")
    configured_static_dist_dir = (os.getenv("CTC_STATIC_DIST_DIR") or "").strip()
    static_dist_dir = configured_static_dist_dir or "static_dist"

    if use_static_dist and Path(static_dist_dir).exists():
        static_dir = static_dist_dir
        fallback_static_dir = "static"
    else:
        static_dir = "static"
        fallback_static_dir = None

    fastapi_app.mount(
        "/static",
        FallbackStaticFiles(directory=static_dir, fallback_directory=fallback_static_dir),
        name="static",
    )

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

        The source-of-truth lives in `static/`, but production may serve from
        `static_dist/` when `CTC_USE_STATIC_DIST=1`.
        """

        static_dist_path = Path(static_dist_dir) / "cv-oliver-ernster.pdf"
        static_src_path = Path("static") / "cv-oliver-ernster.pdf"

        if use_static_dist and static_dist_path.exists():
            return FileResponse(static_dist_path)
        return FileResponse(static_src_path)

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
    fastapi_app.state.templates = Jinja2Templates(env=env)

    @fastapi_app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        resp = FileResponse("static/favicon.ico")
        # Favicons are often cached aggressively by browsers; force revalidation.
        resp.headers["Cache-Control"] = "no-cache, must-revalidate"
        return resp

    fastapi_app.include_router(html_router)
    fastapi_app.include_router(api_router)
    fastapi_app.include_router(rss_router)
    fastapi_app.include_router(sitemap_router)

    return fastapi_app


app = create_app()
