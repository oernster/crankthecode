from __future__ import annotations

"""Leadership / topic hub context builders."""

from typing import cast

from app.domain.tags import (
    extract_layer_slugs_from_tags,
    humanize_layer_slug,
    normalize_layer_slug,
    primary_layer_slug_from_tags,
)
from app.domain.taxonomy import (
    PATTERNS_CAT_TAG,
    PATTERNS_LAYER_LABELS,
)
from app.services.blog_service import BlogService


def is_leadership_post(tags: list[str]) -> bool:
    """Return True if tags include the `cat:Leadership` category."""
    return any((t or "").strip().lower() == "cat:leadership" for t in (tags or []))


def is_patterns_post(tags: list[str]) -> bool:
    return any((t or "").strip().lower() == PATTERNS_CAT_TAG for t in (tags or []))


def topic_descriptions() -> dict[str, str]:
    """Short topic blurbs keyed by normalized `layer:` slug."""
    return {
        "decision-systems": "Decision ownership, option space and the mechanics of stable decisions at scale.",
        "cto-operating-model": "Authority, escalation and operating rhythms that keep execution coherent.",
        "organisational-structure": "Roles, boundaries and structure as the substrate for durable delivery.",
        "structural-design": "Models and primitives for designing organisations that compound rather than fragment.",
        "architecture": "Architecture as boundary design: where constraints live and how systems stay legible.",
    }


def build_leadership_topic_hubs(blog: BlogService) -> list[dict[str, object]]:
    """Derive stable topic hubs from existing `cat:Leadership` + `layer:` tags."""

    layer_counts: dict[str, int] = {}
    for p in blog.list_posts():
        tags = [str(t) for t in (p.tags or [])]
        if not is_leadership_post(tags):
            continue
        layer_slugs = sorted(extract_layer_slugs_from_tags(tags))
        if not layer_slugs:
            layer_slugs = [""]
        for layer_slug in layer_slugs:
            layer_counts[layer_slug] = layer_counts.get(layer_slug, 0) + 1

    preferred_order = [
        "decision-systems",
        "cto-operating-model",
        "organisational-structure",
        "structural-design",
        "architecture",
        "",
    ]

    def _sort_key(slug: str) -> tuple[int, str]:
        if slug in preferred_order:
            return (preferred_order.index(slug), "")
        return (999, humanize_layer_slug(slug).lower())

    descriptions = topic_descriptions()
    hubs: list[dict[str, object]] = []
    for slug in sorted(layer_counts.keys(), key=_sort_key):
        label = humanize_layer_slug(slug) if slug else "General"
        hubs.append(
            {
                "layer": slug,
                "label": label,
                "description": descriptions.get(slug, ""),
                "href": f"/topics/{slug}" if slug else "/topics/general",
                "count": layer_counts.get(slug, 0),
            }
        )

    for h in hubs:
        if h.get("layer") == "":
            h["layer"] = "general"
    return hubs


def topic_layer_slug_for_route(raw: str) -> str:
    """Normalize topic route param.

    `general` is a stable alias for posts with no `layer:`.
    Everything else uses the existing layer normalizer.
    """
    cleaned = (raw or "").strip().lower()
    if cleaned in {"", "general"}:
        return "general"
    return normalize_layer_slug(cleaned)


def topic_posts_for_layer(blog: BlogService, *, layer_slug: str) -> list[dict[str, object]]:
    """Return leadership posts for a given normalized topic `layer_slug`."""
    out: list[dict[str, object]] = []
    for p in blog.list_posts():
        tags = [str(t) for t in (p.tags or [])]
        if not is_leadership_post(tags):
            continue

        primary = primary_layer_slug_from_tags(tags) or ""
        primary = normalize_layer_slug(primary) if primary else ""

        if layer_slug == "general":
            if extract_layer_slugs_from_tags(tags):
                continue
        else:
            if layer_slug not in extract_layer_slugs_from_tags(tags):
                continue

        out.append(
            {
                "slug": p.slug,
                "title": p.title,
                "date": p.date,
                "blurb": getattr(p, "blurb", None),
                "one_liner": getattr(p, "one_liner", None),
                "emoji": getattr(p, "emoji", None),
                "primary_layer": primary,
            }
        )

    out.sort(key=lambda i: str(i.get("date", "")), reverse=True)
    return out


def patterns_posts_for_layer(
    blog: BlogService, *, layer_slug: str
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for p in blog.list_posts():
        tags = [str(t) for t in (p.tags or [])]
        if not is_patterns_post(tags):
            continue

        if layer_slug == "general":
            if extract_layer_slugs_from_tags(tags):
                continue
        else:
            if layer_slug not in extract_layer_slugs_from_tags(tags):
                continue

        out.append(
            {
                "slug": p.slug,
                "title": p.title,
                "date": p.date,
                "emoji": getattr(p, "emoji", None),
                "blurb": getattr(p, "blurb", None),
                "one_liner": getattr(p, "one_liner", None),
            }
        )

    out.sort(key=lambda i: str(i.get("date", "")), reverse=True)
    return out


def homepage_leadership_items(blog: BlogService) -> list[dict[str, object]]:
    """Homepage Leadership content grouped by `layer:`."""
    posts: list[dict[str, object]] = []
    for p in blog.list_posts():
        tags_norm = [(str(t) or "").strip().lower() for t in (p.tags or [])]
        if "cat:leadership" not in tags_norm:
            continue
        posts.append(
            {
                "slug": p.slug,
                "label": p.title,
                "date": str(p.date or ""),
                "tags": [str(t) for t in (p.tags or [])],
            }
        )

    posts.sort(key=lambda i: str(i.get("date", "")), reverse=True)

    layer_to_items: dict[str, list[dict[str, str]]] = {}
    for p in posts:
        tags = [str(t) for t in cast(list[object], (p.get("tags") or []))]
        layer_slugs = sorted(extract_layer_slugs_from_tags(tags))
        if not layer_slugs:
            layer_slugs = [""]

        for layer_slug in layer_slugs:
            layer_to_items.setdefault(layer_slug, [])
            layer_to_items[layer_slug].append(
                {"slug": str(p.get("slug") or ""), "label": str(p.get("label") or "")}
            )

    def layer_sort_key(slug: str) -> str:
        if slug == "":
            return "zzzz-general"
        return humanize_layer_slug(slug).lower()

    out: list[dict[str, object]] = []
    for layer_slug in sorted(layer_to_items.keys(), key=layer_sort_key):
        out.append(
            {
                "layer": layer_slug,
                "label": humanize_layer_slug(layer_slug) if layer_slug else "General",
                "posts": layer_to_items[layer_slug],
            }
        )

    return out


def category_posts_grouped_by_layer(
    blog: BlogService,
    *,
    cat_tag: str,
    layer_label_overrides: dict[str, str] | None = None,
    preferred_layer_order: list[str] | None = None,
) -> list[dict[str, object]]:
    """Group posts for a given `cat:` tag under their `layer:` slugs."""
    cat_norm = (cat_tag or "").strip().lower()
    if not cat_norm:
        return []

    posts: list[dict[str, object]] = []
    for p in blog.list_posts():
        tags_norm = [(str(t) or "").strip().lower() for t in (p.tags or [])]
        if cat_norm not in tags_norm:
            continue
        posts.append(
            {
                "slug": p.slug,
                "label": p.title,
                "date": str(p.date or ""),
                "tags": [str(t) for t in (p.tags or [])],
            }
        )

    posts.sort(key=lambda i: str(i.get("date", "")), reverse=True)

    layer_to_items: dict[str, list[dict[str, str]]] = {}
    for p in posts:
        tags = [str(t) for t in cast(list[object], (p.get("tags") or []))]
        layer_slugs = sorted(extract_layer_slugs_from_tags(tags))
        if not layer_slugs:
            layer_slugs = [""]

        for layer_slug in layer_slugs:
            layer_to_items.setdefault(layer_slug, [])
            layer_to_items[layer_slug].append(
                {"slug": str(p.get("slug") or ""), "label": str(p.get("label") or "")}
            )

    overrides = layer_label_overrides or {}
    preferred = preferred_layer_order or []

    def _layer_label(slug: str) -> str:
        if slug in overrides:
            return overrides[slug]
        return humanize_layer_slug(slug) if slug else "General"

    def _layer_sort_key(slug: str) -> tuple[int, str]:
        if slug in preferred:  # pragma: no cover — no active caller passes preferred_layer_order
            return (preferred.index(slug), "")
        if slug == "":
            return (9999, "zzzz-general")
        return (9999, _layer_label(slug).lower())

    out: list[dict[str, object]] = []
    for layer_slug in sorted(layer_to_items.keys(), key=_layer_sort_key):
        out.append(
            {
                "layer": layer_slug,
                "label": _layer_label(layer_slug),
                "posts": layer_to_items[layer_slug],
            }
        )

    return out
