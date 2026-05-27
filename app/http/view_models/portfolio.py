from __future__ import annotations

"""Portfolio context builders."""

from pathlib import Path

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.http.view_models.posts import (
    is_project_post_by_tags,
    post_emoji_map,
    post_frontmatter_emoji_index,
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


def _items_from_summaries(
    *,
    summaries: list[object],
    emoji_map: dict[str, str],
    emoji_index: dict[str, str],
) -> list[dict[str, object]]:
    return [
        portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in summaries
    ]


def portfolio_groups(blog: BlogService) -> list[dict[str, object]]:
    """Build the Portfolio page groups.

    Requirements:
    - no pinning/curation (purely derived from post metadata)
    - each section is date-desc sorted
    """
    emoji_map = post_emoji_map()
    emoji_index = post_frontmatter_emoji_index(blog)

    hidden = {"about-me", "start-here", "portfolio"}

    data_summaries: list[object] = []
    desktop_summaries: list[object] = []
    gaming_summaries: list[object] = []
    hardware_summaries: list[object] = []
    tools_summaries: list[object] = []
    webapi_summaries: list[object] = []
    for p in blog.list_posts():
        slug = str(getattr(p, "slug", "") or "").strip().lower()
        if not slug or slug in hidden:
            continue

        tags = [str(t) for t in (getattr(p, "tags", []) or [])]
        post_type = str(getattr(p, "post_type", "") or "")
        if not is_project_post_by_tags(post_type, tags):
            continue

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

    desktop_items = _items_from_summaries(
        summaries=desktop_summaries,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )
    tools_items = _items_from_summaries(
        summaries=tools_summaries,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )
    hardware_items = _items_from_summaries(
        summaries=hardware_summaries,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )
    data_items = _items_from_summaries(
        summaries=data_summaries,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )
    gaming_items = _items_from_summaries(
        summaries=gaming_summaries,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )
    webapi_items = _items_from_summaries(
        summaries=webapi_summaries,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )

    return [
        {
            "label": "Desktop Applications",
            "description": "Independent desktop systems (UI + local operations).",
            "entries": desktop_items,
        },
        {
            "label": "Operational Tools",
            "description": "Systems and tools designed to support real operational work under load.",
            "entries": tools_items,
        },
        {
            "label": "Data / ML",
            "description": "Data-oriented experiments (small, focused systems).",
            "entries": data_items,
        },
        {
            "label": "Gaming",
            "description": "Gaming-adjacent systems and community tooling.",
            "entries": gaming_items,
        },
        {
            "label": "Hardware / Embedded",
            "description": "Embedded and physical-system experiments; practical boundary work.",
            "entries": hardware_items,
        },
        {
            "label": "Web APIs",
            "description": "Small APIs and backend experiments.",
            "entries": webapi_items,
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
