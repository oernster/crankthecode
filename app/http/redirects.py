"""Legacy-URL redirect table.

One table, consulted by a single middleware in `app.main`, instead of
per-route redirect handlers scattered across routers.

Sources of truth:
- `REMOVED_POST_SLUGS`: essays culled in the Selected Essays restructure.
  Their content lives on in the books, so each old post URL lands on /books.
- `RETIRED_TOPIC_SLUGS`: the Decision Architecture topic taxonomy, replaced
  by the curated /essays page.
"""

from __future__ import annotations

from typing import Mapping

ESSAYS_PATH = "/essays"
BUILD_LOG_PATH = "/build-log"
BOOKS_PATH = "/books"

REMOVED_POST_SLUGS: tuple[str, ...] = (
    "lead1",
    "lead3",
    "lead5",
    "lead7",
    "lead8",
    "lead9",
    "lead10",
    "lead11",
    "lead12",
    "lead13",
    "lead14",
    "lead15",
    "lead16",
    "lead18",
    "lead19",
    "lead20",
    "lead22",
    "lead23",
    "lead24",
    "lead25",
    "lead26",
    "lead31",
)

RETIRED_TOPIC_SLUGS: tuple[str, ...] = (
    "architecture",
    "cto-operating-model",
    "decision-systems",
    "organisational-structure",
    "structural-design",
)

REDIRECT_TABLE: dict[str, str] = {
    "/decision-architecture": ESSAYS_PATH,
    "/topics": ESSAYS_PATH,
    "/writing": ESSAYS_PATH,
    **{f"/topics/{slug}": ESSAYS_PATH for slug in RETIRED_TOPIC_SLUGS},
    **{f"/posts/{slug}": BOOKS_PATH for slug in REMOVED_POST_SLUGS},
}

_POSTS_PATH = "/posts"
_VIEW_WRITING = "writing"
_CAT_BLOG = "blog"


def resolve_redirect(path: str, query_params: Mapping[str, str]) -> str | None:
    """Return a 301 target for a legacy URL; None falls through.

    Exact-path lookups come from `REDIRECT_TABLE`. The old /posts views are
    matched on their query string: `view=writing` lands on /essays and
    `view=writing&cat=Blog` lands on /build-log. A query that also carries a
    search (`q`) or a layer filter is a live filter, not a legacy view, so it
    falls through to the /posts page.
    """

    cleaned = (path or "").rstrip("/") or "/"

    target = REDIRECT_TABLE.get(cleaned)
    if target:
        return target

    if cleaned != _POSTS_PATH:
        return None

    view = (query_params.get("view") or "").strip().lower()
    if view != _VIEW_WRITING:
        return None
    if (query_params.get("q") or "").strip():
        return None
    if (query_params.get("layer") or "").strip():
        return None

    cat = (query_params.get("cat") or "").strip().lower()
    if not cat:
        return ESSAYS_PATH
    if cat == _CAT_BLOG:
        return BUILD_LOG_PATH
    return None
