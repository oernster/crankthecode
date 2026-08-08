"""View-model assembly for the posts index page.

The route handler keeps request parsing and the template call. Turning posts
into listing rows, narrowing them by category and layer and naming the page all
happen here, where none of it needs a request to exercise.
"""

from __future__ import annotations

from typing import Any

from app.domain.tags import extract_layer_slugs_from_tags, normalize_layer_slug
from app.http.view_models.posts import (
    display_title_parts,
    post_emoji_map,
    split_leading_emoji_from_title,
)
from app.http.view_models.sidebar import (
    extract_category_queries_from_tags,
    normalize_cat_label,
    posts_base_href,
    posts_href,
)

# Pages that have their own route and are not listing entries.
_HIDDEN_SLUGS = frozenset({"about-me", "about", "start-here", "portfolio"})

_CAT_TAG_PREFIX = "cat:"

_SITE_NAME = "Crank The Code"
_DEFAULT_TITLE = f"Posts | {_SITE_NAME}"
_DEFAULT_DESCRIPTION = f"Browse all {_SITE_NAME} posts and project write-ups."


def _tag_strings(row: dict[str, Any]) -> list[str]:
    return [str(t) for t in (row.get("tags") or [])]


def resolve_cat_label(*, current_cat: str, current_q: str) -> str | None:
    """Read the active category from the `cat` param or a `cat:` search query.

    The `q=cat:<Label>` form is the older deeplink and is still honoured, so
    both spellings have to resolve to the same normalised label.
    """

    if current_cat:
        return normalize_cat_label(current_cat)

    lowered = current_q.lower()
    if lowered.startswith(_CAT_TAG_PREFIX) and lowered.strip() != _CAT_TAG_PREFIX:
        tail = current_q.split(":", 1)[1].strip()
        return normalize_cat_label(tail) if tail else None

    return None


def build_index_breadcrumbs(
    *,
    view: str,
    cat_label: str | None,
    category_label: str | None,
    layer_label: str | None,
    filtered_href: str,
) -> list[dict[str, str]]:
    """Home, then Posts, then whichever filters are actually active."""

    items = [
        {"label": "Home", "href": "/"},
        {"label": "Posts", "href": posts_base_href(view=view)},
    ]

    if cat_label:
        items.append(
            {
                "label": category_label or cat_label,
                "href": posts_href(
                    query=None, cat=cat_label, layer=None, exclude_blog=None
                ),
            }
        )
        if layer_label:
            items.append({"label": layer_label, "href": filtered_href})

    return items


def build_index_rows(blog: Any) -> list[dict[str, Any]]:
    """Flatten every listed post into the shape `posts.html` expects."""

    emoji_map = post_emoji_map()
    rows: list[dict[str, Any]] = []

    for post in blog.list_posts():
        emoji, title_text = display_title_parts(
            title=post.title,
            emoji=getattr(post, "emoji", None) or emoji_map.get(post.slug, ""),
        )
        rows.append(
            {
                "slug": post.slug,
                "title": post.title,
                "title_text": title_text,
                "date": post.date,
                "tags": list(post.tags),
                "post_type": getattr(post, "post_type", None),
                "blurb": getattr(post, "blurb", None),
                "one_liner": getattr(post, "one_liner", None),
                "cover_image_url": post.cover_image_url,
                "thumb_image_url": getattr(post, "thumb_image_url", None),
                "emoji": emoji,
                "summary_html": post.summary_html,
            }
        )

    return [
        row
        for row in rows
        if str(row.get("slug", "")).strip().lower() not in _HIDDEN_SLUGS
    ]


def filter_rows_by_cat(
    rows: list[dict[str, Any]], cat_label: str
) -> list[dict[str, Any]]:
    """Keep only rows carrying the given category, compared normalised."""

    wanted = f"cat:{normalize_cat_label(cat_label)}".strip().lower()
    return [
        row
        for row in rows
        if any(
            (query or "").strip().lower() == wanted
            for query in extract_category_queries_from_tags(_tag_strings(row))
        )
    ]


def filter_rows_by_layer(
    rows: list[dict[str, Any]], layer_slug: str
) -> list[dict[str, Any]]:
    """Keep only rows carrying the given layer, compared normalised."""

    wanted = f"layer:{normalize_layer_slug(layer_slug)}".strip().lower()
    return [
        row
        for row in rows
        if any(
            f"layer:{slug}".strip().lower() == wanted
            for slug in extract_layer_slugs_from_tags(_tag_strings(row))
        )
    ]


def build_index_titles(
    *,
    cat_label: str | None,
    category_label: str | None,
    layer_label: str | None,
) -> dict[str, str]:
    """Name the page after whatever narrowed it, or leave the default."""

    titles = {
        "page_title": _DEFAULT_TITLE,
        "og_title": _DEFAULT_TITLE,
        "og_description": _DEFAULT_DESCRIPTION,
        "meta_description": _DEFAULT_DESCRIPTION,
    }

    if not cat_label:
        return titles

    cat_display = (category_label or cat_label).strip()
    _, cat_text = split_leading_emoji_from_title(cat_display)
    cat_text = (cat_text or cat_display).strip()

    if layer_label:
        page_title = f"{layer_label} | {cat_text} | Posts | {_SITE_NAME}"
        description = f"Browse posts in {layer_label} ({cat_text}) on {_SITE_NAME}."
    elif cat_text:
        page_title = f"{cat_text} | Posts | {_SITE_NAME}"
        description = f"Browse posts in {cat_text} on {_SITE_NAME}."
    else:
        # A category that normalises to nothing keeps the default naming.
        return titles  # pragma: no cover

    titles.update(
        {
            "page_title": page_title,
            "og_title": page_title,
            "og_description": description,
            "meta_description": description,
        }
    )
    return titles
