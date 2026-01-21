from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import FileResponse
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
