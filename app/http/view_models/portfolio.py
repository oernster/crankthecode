from __future__ import annotations

"""Portfolio context builders."""

from pathlib import Path

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.http.view_models.posts import (
    post_emoji_map,
    post_frontmatter_emoji_index,
    post_summary_index,
)
from app.services.blog_service import BlogService


def has_cat_tag(tags: list[str], cat_label: str) -> bool:
    target = f"cat:{(cat_label or '').strip().lower()}"
    return any((t or "").strip().lower() == target for t in (tags or []))


def has_any_cat_tag(tags: list[str], cat_labels: list[str]) -> bool:
    return any(has_cat_tag(tags, lbl) for lbl in (cat_labels or []))


def portfolio_item_from_summary(
    *,
    summary: object,
    emoji_map: dict[str, str],
    frontmatter_emoji_index: dict[str, str],
) -> dict[str, object]:
    slug = str(getattr(summary, "slug", "") or "").strip()
    slug_key = slug.lower()
    emoji = (frontmatter_emoji_index.get(slug) or frontmatter_emoji_index.get(slug_key) or "").strip()
    if not emoji:
        emoji = (emoji_map.get(slug) or emoji_map.get(slug_key) or "").strip()

    return {
        "slug": slug,
        "label": str(getattr(summary, "title", "") or slug),
        "blurb": getattr(summary, "blurb", None),
        "cover_image_url": getattr(summary, "cover_image_url", None),
        "thumb_image_url": getattr(summary, "thumb_image_url", None),
        "emoji": emoji,
        "role": getattr(summary, "role", None),
    }


def curated_portfolio_entries_from_slugs(
    *,
    slugs: list[str],
    index: dict[str, object],
    hidden: set[str],
    emoji_map: dict[str, str],
    emoji_index: dict[str, str],
) -> list[dict[str, object]]:
    """Convert a curated list of slugs into Portfolio entries."""
    entries: list[dict[str, object]] = []
    for raw in slugs:
        key = (str(raw or "")).strip().lower()
        if not key or key in hidden:
            continue
        summary = index.get(key)
        if summary is None:
            continue
        entries.append(
            portfolio_item_from_summary(
                summary=summary,
                emoji_map=emoji_map,
                frontmatter_emoji_index=emoji_index,
            )
        )
    return entries


def portfolio_flagship_entries(blog: BlogService) -> list[dict[str, object]]:
    """Return portfolio entries for any project(s) with `role: flagship`."""
    emoji_map = post_emoji_map()
    emoji_index = post_frontmatter_emoji_index(blog)

    out: list[dict[str, object]] = []
    for p in blog.list_posts():
        post_type = str(getattr(p, "post_type", "") or "").strip().lower()
        if post_type != "project":
            continue
        role = str(getattr(p, "role", "") or "").strip().lower()
        if role != "flagship":
            continue
        out.append(
            portfolio_item_from_summary(
                summary=p,
                emoji_map=emoji_map,
                frontmatter_emoji_index=emoji_index,
            )
        )
    return out


def portfolio_groups(blog: BlogService) -> list[dict[str, object]]:
    """Build the curated Portfolio page groups."""
    emoji_map = post_emoji_map()
    emoji_index = post_frontmatter_emoji_index(blog)
    index = post_summary_index(blog)

    hidden = {"about-me", "start-here", "portfolio"}

    flagship_slugs: set[str] = set()
    for p in blog.list_posts():
        post_type = str(getattr(p, "post_type", "") or "").strip().lower()
        if post_type != "project":
            continue
        role = str(getattr(p, "role", "") or "").strip().lower()
        if role == "flagship":
            slug = str(getattr(p, "slug", "") or "").strip().lower()
            if slug:
                flagship_slugs.add(slug)

    desktop_items = curated_portfolio_entries_from_slugs(
        slugs=[
            "clearbudget",
            "commanddeck",
            "trainer",
            "calendifier",
            "stellody",
            "fancy-clock",
            "elevator",
        ],
        index=index,
        hidden=hidden,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )

    curated_slugs = {e.get("slug", "") for e in [*desktop_items]}
    curated_slugs = {str(s).strip().lower() for s in curated_slugs if str(s).strip()}
    curated_slugs |= flagship_slugs

    data_summaries: list[object] = []
    desktop_summaries: list[object] = []
    gaming_summaries: list[object] = []
    hardware_summaries: list[object] = []
    tools_summaries: list[object] = []
    webapi_summaries: list[object] = []
    for p in blog.list_posts():
        slug = str(getattr(p, "slug", "") or "").strip().lower()
        if not slug or slug in hidden or slug in curated_slugs:
            continue
        tags = [str(t) for t in (getattr(p, "tags", []) or [])]
        if has_cat_tag(tags, "Desktop Apps"):
            desktop_summaries.append(p)
        if has_any_cat_tag(tags, ["Data / Ml", "Data / ML"]):
            data_summaries.append(p)
        if has_cat_tag(tags, "Gaming"):
            gaming_summaries.append(p)
        if has_cat_tag(tags, "Hardware"):
            hardware_summaries.append(p)
        if has_cat_tag(tags, "Tools"):
            tools_summaries.append(p)
        if has_any_cat_tag(tags, ["Web Apis", "Web APIs"]):
            webapi_summaries.append(p)

    def date_key(p: object) -> str:
        return str(getattr(p, "date", "") or "")

    data_summaries.sort(key=date_key, reverse=True)
    desktop_summaries.sort(key=date_key, reverse=True)
    gaming_summaries.sort(key=date_key, reverse=True)
    hardware_summaries.sort(key=date_key, reverse=True)
    tools_summaries.sort(key=date_key, reverse=True)
    webapi_summaries.sort(key=date_key, reverse=True)

    pinned_hardware = []
    rest_hardware = []
    for p in hardware_summaries:
        if str(getattr(p, "slug", "") or "").strip().lower() == "galacticunicorn":
            pinned_hardware.append(p)
        else:
            rest_hardware.append(p)
    hardware_items = [
        portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in (pinned_hardware + rest_hardware)
    ]

    pinned_tools = curated_portfolio_entries_from_slugs(
        slugs=["audiodeck"],
        index=index,
        hidden=hidden,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )
    tools_items = pinned_tools + [
        portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in tools_summaries
    ]

    seen: set[str] = set()
    tools_items_deduped: list[dict[str, object]] = []
    for it in tools_items:
        slug = str(it.get("slug") or "").strip().lower()
        if not slug or slug in seen:
            continue
        seen.add(slug)
        tools_items_deduped.append(it)

    data_items = [
        portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in data_summaries
    ]
    gaming_items = [
        portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in gaming_summaries
    ]
    webapi_items = [
        portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in webapi_summaries
    ]

    return [
        {
            "label": "Desktop Applications",
            "description": "Independent desktop systems (UI + local operations).",
            "entries": desktop_items,
            "more_href": "/posts?cat=Desktop%20Apps",
        },
        {
            "label": "Web APIs",
            "description": "Small APIs and backend experiments.",
            "entries": webapi_items,
            "more_href": "/posts?cat=Web%20Apis",
        },
        {
            "label": "Data / ML",
            "description": "Data-oriented experiments (small, focused systems).",
            "entries": data_items,
            "more_href": "/posts?cat=Data%20/%20Ml",
        },
        {
            "label": "Gaming",
            "description": "Gaming-adjacent systems and community tooling.",
            "entries": gaming_items,
            "more_href": "/posts?cat=Gaming",
        },
        {
            "label": "Hardware / Embedded",
            "description": "Embedded and physical-system experiments; practical boundary work.",
            "entries": hardware_items,
            "more_href": "/posts?cat=Hardware",
        },
        {
            "label": "Operational Tools",
            "description": "Systems and tools designed to support real operational work under load.",
            "entries": tools_items_deduped,
            "more_href": "/posts?cat=Tools",
        },
    ]


def load_portfolio_post() -> object | None:
    """Load the `posts/portfolio.md` page content (markdown + frontmatter)."""
    try:
        repo = FilesystemPostsRepository(posts_dir=Path("posts"))
        return repo.get_post("portfolio")
    except Exception:
        return None


def render_portfolio_intro_html() -> str:
    post = load_portfolio_post()
    if post is None:
        return ""
    try:
        return PythonMarkdownRenderer().render(getattr(post, "content_markdown", "") or "")
    except Exception:
        return ""


def portfolio_label_to_slug(label: str) -> str:
    """Convert a portfolio group label to a URL-safe slug."""
    return label.lower().replace(" / ", "-").replace(" ", "-")
