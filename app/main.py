from __future__ import annotations

from typing import Awaitable, Callable

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

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

    # Static and templates
    fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")
    fastapi_app.mount("/docs", StaticFiles(directory="docs"), name="docs")

    # Templates
    # - auto_reload + cache_size=0 ensures template edits are reflected without restarting the server
    #   (useful during local dev; acceptable overhead for this small site).
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=True,
        auto_reload=True,
        cache_size=0,
    )
    fastapi_app.state.templates = Jinja2Templates(env=env)

    @fastapi_app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return FileResponse("static/favicon.ico")

    fastapi_app.include_router(html_router)
    fastapi_app.include_router(api_router)
    fastapi_app.include_router(rss_router)
    fastapi_app.include_router(sitemap_router)

    return fastapi_app


app = create_app()
