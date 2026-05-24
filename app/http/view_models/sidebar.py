from __future__ import annotations

"""Sidebar context builders and shared URL/tag utilities.

These helpers are used by multiple routers. They have no dependency on
FastAPI routing objects — only on domain models and blog service.
"""

from typing import cast
from urllib.parse import quote

from app.domain.tags import (
    extract_layer_slugs_from_tags,
    humanize_layer_slug,
    normalize_layer_slug,
)
from app.services.blog_service import BlogService

_CAT_TAG_PREFIX = "cat:"
_CAT_TAG_BLOG = "cat:blog"
_LAYER_TAG_PREFIX = "layer:"

_TRUTHY_QUERY: frozenset[str] = frozenset({"1", "true", "yes", "y", "on"})
_FALSY_QUERY: frozenset[str] = frozenset({"0", "false", "no", "n", "off"})

# /posts filter view names
POSTS_VIEW_WRITING = "writing"
POSTS_VIEW_PROJECTS = "projects"
POSTS_VIEW_ARCHIVE = "archive"
POSTS_ALLOWED_VIEWS: frozenset[str] = frozenset({
    POSTS_VIEW_WRITING,
    POSTS_VIEW_PROJECTS,
    POSTS_VIEW_ARCHIVE,
})


def normalize_cat_label(raw_label: str) -> str:
    """Normalize `cat:` labels for display.

    Rules:
    - collapse whitespace
    - Title Case

    Note: intentionally does *not* preserve acronyms (e.g. "APIs" -> "Apis")
    to match the requested behavior.
    """
    cleaned = " ".join((raw_label or "").strip().split())
    return cleaned.title()


def extract_category_queries_from_tags(tags: list[str]) -> set[str]:
    """Extract normalized `cat:` category queries from a post's tag list."""
    out: set[str] = set()
    for t in tags or []:
        raw = (t or "").strip()
        if not raw:
            continue
        if not raw.lower().startswith(_CAT_TAG_PREFIX):
            continue
        tail = raw.split(":", 1)[1].strip()
        if not tail:
            continue
        label = normalize_cat_label(tail)
        out.add(f"cat:{label}".strip())
    return out


def is_blog_post_by_cat(tags: list[str]) -> bool:
    return any((t or "").strip().lower() == _CAT_TAG_BLOG for t in (tags or []))


def posts_href(
    *,
    query: str | None,
    exclude_blog: bool | None,
    cat: str | None = None,
    layer: str | None = None,
) -> str:
    parts: list[str] = []
    if query:
        parts.append(f"q={quote(query, safe='')}")
    if cat:
        parts.append(f"cat={quote(cat, safe='')}")
    if layer:
        parts.append(f"layer={quote(layer, safe='')}")
    if exclude_blog is not None:
        parts.append(f"exclude_blog={'1' if exclude_blog else '0'}")
    return "/posts" + ("?" + "&".join(parts) if parts else "")


def posts_view_href(
    *,
    view: str,
    query: str | None,
    cat: str | None = None,
    layer: str | None = None,
) -> str:
    """Build a /posts href preserving secondary filters.

    Primary filter is `view=writing|projects|archive`.
    Secondary filters remain `q`, `cat`, `layer`.
    """
    parts: list[str] = [f"view={quote(view, safe='')}"]
    if query:
        parts.append(f"q={quote(query, safe='')}")
    if cat:
        parts.append(f"cat={quote(cat, safe='')}")
    if layer:
        parts.append(f"layer={quote(layer, safe='')}")
    return "/posts" + ("?" + "&".join(parts) if parts else "")


def posts_base_href(*, view: str | None = None) -> str:
    """Canonical breadcrumb href for the Posts listing."""
    view_norm = normalize_posts_view(view)
    if not view_norm:
        return "/posts"
    return f"/posts?view={quote(view_norm, safe='')}"


def normalize_posts_view(raw: str | None) -> str:
    view = (raw or "").strip().lower()
    return view if view in POSTS_ALLOWED_VIEWS else ""


def posts_view_from_legacy_exclude_blog(raw: str | None) -> str | None:
    """Backwards compatibility for legacy links.

    Mapping:
    - exclude_blog=1 -> view=projects
    - exclude_blog=0 -> view=archive

    Only used when `view` is absent.
    """
    val = (raw or "").strip().lower()
    if not val:
        return None
    if val in _TRUTHY_QUERY:
        return POSTS_VIEW_PROJECTS
    if val in _FALSY_QUERY:
        return POSTS_VIEW_ARCHIVE
    return None


def sidebar_label_with_emoji(label: str) -> str:
    """Decorate known sidebar category labels with their legacy emoji.

    Category *queries* remain `cat:<Label>`; this is purely display polish.
    Labels passed here are already normalized (Title Case).
    """
    key = (label or "").strip().lower()
    if not key:
        return label

    mapping = {
        "blog": "📝 Blog",
        "automation": "🤖 Automation",
        "data / ml": "🧠 Data / ML",
        "desktop apps": "🖥️ Desktop Apps",
        "gaming": "🎮 Gaming",
        "governance": "🏛️ Governance",
        "hardware": "🔧 Hardware",
        "leadership": "♟️ Decision Architecture",
        "tools": "🧰 Tools",
        "web apis": "🌐 Web APIs",
    }
    return mapping.get(key, label)


def build_sidebar_categories(
    blog: BlogService, *, exclude_blog: bool
) -> list[dict[str, object]]:
    """Build sidebar categories from explicit `cat:` tags and nested `layer:` tags."""

    cats: dict[str, dict[str, object]] = {}

    for p in blog.list_posts():
        tags = [str(t) for t in (p.tags or [])]
        cat_queries = extract_category_queries_from_tags(tags)
        if not cat_queries:
            continue

        layers = extract_layer_slugs_from_tags(tags)
        for q in cat_queries:
            cat_label = q.split(":", 1)[1].strip() if ":" in q else q
            cat_label_norm = normalize_cat_label(cat_label)

            key = cat_label_norm.lower()
            entry = cats.get(key)
            if entry is None:
                entry = {
                    "cat": cat_label_norm,
                    "query": f"cat:{cat_label_norm}",
                    "label": sidebar_label_with_emoji(cat_label_norm),
                    "layers_map": {},
                }
                cats[key] = entry

            layers_map = cast(dict[str, dict[str, str]], entry["layers_map"])
            for layer_slug in layers:
                layers_map.setdefault(
                    layer_slug,
                    {
                        "layer": layer_slug,
                        "label": humanize_layer_slug(layer_slug),
                    },
                )

    def category_sort_key(entry: dict[str, object]) -> tuple[int, str]:
        cat_label = str(entry.get("cat", "")).strip()
        cat_norm = cat_label.lower()
        is_decision_architecture = cat_norm == "leadership"
        return (0 if is_decision_architecture else 1, cat_norm)

    out: list[dict[str, object]] = []
    for entry in sorted(cats.values(), key=category_sort_key):
        cat_label_norm = str(entry.get("cat") or "")
        cat_is_blog = cat_label_norm.strip().lower() == "blog"
        href_exclude_blog = (
            False if cat_is_blog else (False if not exclude_blog else None)
        )

        layers_map = cast(dict[str, dict[str, str]], entry.pop("layers_map", {}))
        layers = sorted(
            layers_map.values(), key=lambda d: (d.get("label") or "").lower()
        )

        out.append(
            {
                "cat": cat_label_norm,
                "query": entry.get("query"),
                "label": entry.get("label"),
                "href": posts_href(
                    query=None,
                    cat=cat_label_norm,
                    layer=None,
                    exclude_blog=href_exclude_blog,
                ),
                "layers": [
                    {
                        "layer": layer_entry["layer"],
                        "label": layer_entry["label"],
                        "href": posts_href(
                            query=None,
                            cat=cat_label_norm,
                            layer=layer_entry["layer"],
                            exclude_blog=href_exclude_blog,
                        ),
                    }
                    for layer_entry in layers
                    if layer_entry.get("layer")
                ],
            }
        )

    return out
