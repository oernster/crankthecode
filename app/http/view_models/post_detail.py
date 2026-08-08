"""View-model assembly for the post detail page.

The route handler is left with request parsing, the redirect and 404 decisions
and the template call. Everything that turns a `PostDetail` into template
context lives here, where it can be read and tested without a request.
"""

from __future__ import annotations

from typing import Any

from app.domain.essays import ESSAY_SLUGS
from app.http.seo import absolute_url, build_meta_description, to_iso_date
from app.http.view_models.posts import display_title_parts

_CAT_TAG_PREFIX = "cat:"
_ESSAY_CAT = "cat:leadership"
_PATTERNS_CAT = "cat:decision-architecture-patterns"

_DEFAULT_SOCIAL_IMAGE = "/static/images/me.jpg"
_SCHEMA_CONTEXT = "https://schema.org"
_AUTHOR: dict[str, str] = {"@type": "Person", "name": "Oliver Ernster"}


def build_post_row(detail: Any) -> dict[str, Any]:
    """Flatten a `PostDetail` into the shape `post.html` expects."""

    emoji, title_text = display_title_parts(
        title=detail.title,
        emoji=getattr(detail, "emoji", None),
    )
    return {
        "slug": detail.slug,
        "title": detail.title,
        "title_text": title_text,
        "emoji": emoji,
        "date": detail.date,
        "tags": list(detail.tags),
        "blurb": getattr(detail, "blurb", None),
        "one_liner": getattr(detail, "one_liner", None),
        "cover_image_url": detail.cover_image_url,
        "thumb_image_url": getattr(detail, "thumb_image_url", None),
        "extra_image_urls": list(getattr(detail, "extra_image_urls", [])),
        "content": detail.content_html,
    }


def first_cat_tag(tags: list[str]) -> str:
    """Return the first `cat:` tag as written, or an empty string."""

    for tag in tags or []:
        candidate = str(tag or "").strip()
        if candidate.lower().startswith(_CAT_TAG_PREFIX):
            return candidate
    return ""


def is_essay_post(detail: Any, cat_tag: str) -> bool:
    """An essay either carries the Leadership category or is a named slug."""

    return cat_tag.lower() == _ESSAY_CAT or (
        (detail.slug or "").strip().lower() in ESSAY_SLUGS
    )


def build_navigation(detail: Any, *, cat_tag: str, is_essay: bool) -> dict[str, Any]:
    """Return the back link and breadcrumb trail for a post.

    A post belongs to exactly one hub, so the trail it shows and the place its
    back link returns to are the same decision made once.
    """

    if is_essay:
        hub_label, hub_href = "Selected Essays", "/essays"
        back_label = "← Back to essays"
    elif cat_tag.lower() == _PATTERNS_CAT:
        hub_label, hub_href = "Decision Architecture Patterns", "/patterns"
        back_label = "← Back to Patterns"
    else:
        hub_label, hub_href = "Posts", "/posts"
        back_label = "← Back to posts"

    return {
        "back_link_href": hub_href,
        "back_link_label": back_label,
        "breadcrumb_items": [
            {"label": "Home", "href": "/"},
            {"label": hub_label, "href": hub_href},
            {"label": detail.title, "href": f"/posts/{detail.slug}"},
        ],
    }


def build_descriptions(detail: Any) -> tuple[str, str]:
    """Return the (meta description, og description) pair for a post."""

    description = build_meta_description(
        getattr(detail, "blurb", None),
        fallback=getattr(detail, "one_liner", None),
        default=f"Read {detail.title} on Crank The Code.",
    )
    og_description = build_meta_description(
        getattr(detail, "one_liner", None),
        fallback=getattr(detail, "blurb", None),
        default=description,
    )
    return description, og_description


def build_og_title(detail: Any) -> str:
    """Title for social cards: the post title plus its subtitle when it has one."""

    subtitle = (
        getattr(detail, "one_liner", None) or getattr(detail, "blurb", None) or ""
    ).strip()
    return f"{detail.title} - {subtitle}" if subtitle else detail.title


def build_og_image(detail: Any, *, site_url: str) -> str:
    """Absolute social image URL, falling back to the site portrait."""

    candidate = (
        getattr(detail, "social_image_url", None)
        or detail.cover_image_url
        or absolute_url(site_url, _DEFAULT_SOCIAL_IMAGE)
    )
    return absolute_url(site_url, candidate)


def build_article_jsonld(
    detail: Any, *, canonical: str, description: str, site_url: str
) -> dict[str, Any]:
    """BlogPosting JSON-LD, omitting fields the post does not carry."""

    jsonld: dict[str, object] = {
        "@context": _SCHEMA_CONTEXT,
        "@type": "BlogPosting",
        "headline": detail.title,
        "author": _AUTHOR,
        "mainEntityOfPage": canonical,
        "url": canonical,
        "description": description,
    }

    published_iso = to_iso_date(detail.date)
    if published_iso:
        jsonld["datePublished"] = published_iso
        jsonld["dateModified"] = published_iso

    if detail.cover_image_url:
        jsonld["image"] = [absolute_url(site_url, detail.cover_image_url)]

    tags = [str(t).strip() for t in (detail.tags or []) if str(t).strip()]
    if tags:
        jsonld["keywords"] = ", ".join(tags)

    return jsonld


def build_breadcrumb_jsonld(
    detail: Any, *, canonical: str, site_url: str, is_essay: bool
) -> dict[str, Any]:
    """BreadcrumbList JSON-LD routed through the post's own hub.

    Essays go via /essays so crawlers see a hub-and-spoke graph now that the
    topic hubs are retired.
    """

    hub_name, hub_path = (
        ("Selected Essays", "/essays") if is_essay else ("Posts", "/posts")
    )
    return {
        "@context": _SCHEMA_CONTEXT,
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": absolute_url(site_url, "/"),
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": hub_name,
                "item": absolute_url(site_url, hub_path),
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": detail.title,
                "item": canonical,
            },
        ],
    }
