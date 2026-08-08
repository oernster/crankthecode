"""HTML router aggregator.

All routes are defined in sub-modules and included here so that
`app/main.py` can continue to import a single `router` object.

Sub-module layout:
  pages.py     -- homepage, about, explore, battlestation, redirects
  posts.py     -- /posts listing and /posts/{slug} detail
  essays.py    -- /essays and /build-log
  portfolio.py -- /portfolio
  books.py     -- /books
  topics.py    -- /patterns and /patterns/{layer}
"""

from __future__ import annotations

from fastapi import APIRouter

from app.http.routers.books import router as books_router
from app.http.routers.essays import router as essays_router
from app.http.routers.pages import router as pages_router
from app.http.routers.portfolio import router as portfolio_router
from app.http.routers.posts import router as posts_router
from app.http.routers.topics import router as topics_router

router = APIRouter()
router.include_router(pages_router)
router.include_router(posts_router)
router.include_router(essays_router)
router.include_router(portfolio_router)
router.include_router(books_router)
router.include_router(topics_router)
