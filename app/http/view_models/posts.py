from __future__ import annotations

"""Post display helpers and context builders."""

import math
import re
import unicodedata
from pathlib import Path
from typing import cast

from app.domain.taxonomy import (
    ARCHIVE_CAT_BUCKETS,
    WRITING_CAT_BUCKETS,
    PROJECT_CATEGORY_LABELS,
)
from app.domain.tags import extract_layer_slugs_from_tags
from app.http.view_models.sidebar import (
    POSTS_VIEW_ARCHIVE,
    POSTS_VIEW_WRITING,
    extract_category_queries_from_tags,
    normalize_cat_label,
    sidebar_label_with_emoji,
    build_sidebar_categories,
)
from app.services.blog_service import BlogService

# Max pills shown per category group before a per-group "More..." button appears.
PILL_GROUP_SIZE = 10

# Average silent reading speed for technical content (words per minute).
_WORDS_PER_MINUTE = 200


def estimate_read_time_minutes(content_html: str) -> int:
    """Estimate reading time in minutes from HTML content.

    Strips HTML tags to get plain text, counts words, divides by reading speed.
    Returns a minimum of 1 minute.
    """
    text = re.sub(r"<[^>]+>", " ", content_html or "")
    words = len(text.split())
    return max(1, math.ceil(words / _WORDS_PER_MINUTE))


def estimate_read_time_from_template(template_name: str) -> int:
    """Estimate reading time from a Jinja2 template file.

    Strips Jinja2 syntax and HTML tags, counts plain-text words.
    Used for pages whose content lives in the template rather than a markdown post.
    Falls back to 1 minute if the template cannot be read.
    """
    try:
        raw = (Path("templates") / template_name).read_text(encoding="utf-8")
        # Strip Jinja2 blocks, expressions and comments.
        text = re.sub(r"\{%.*?%\}|\{\{.*?\}\}|\{#.*?#\}", " ", raw, flags=re.DOTALL)
        # Strip HTML tags.
        text = re.sub(r"<[^>]+>", " ", text)
        words = len(text.split())
        return max(1, math.ceil(words / _WORDS_PER_MINUTE))
    except Exception:
        return 1


def split_leading_emoji_from_title(title: str) -> tuple[str | None, str]:
    """Split a leading emoji from a title.

    We use a heuristic rather than a full emoji grapheme parser.

    Rules:
    - If the first whitespace-delimited token looks like an emoji (Unicode symbol
      plus optional variation selector), treat it as the emoji.
    - Otherwise return (None, title).
    """
    raw = (title or "").strip()
    if not raw:
        return None, ""

    token, sep, rest = raw.partition(" ")
    if not token or len(token) > 6:
        return None, raw

    def is_emojiish(ch: str) -> bool:
        if not ch or ord(ch) < 0x80:
            return False
        cat = unicodedata.category(ch)
        return cat in {"So", "Sk"}

    has_symbol = any(is_emojiish(c) for c in token)
    if not has_symbol:
        return None, raw

    emoji = token
    title_text = rest.strip() if sep else ""
    return emoji, title_text or raw


def display_title_parts(*, title: str, emoji: str | None) -> tuple[str, str]:
    """Return (emoji, title_text) for display without duplication.

    Preference order:
    1) Explicit frontmatter `emoji` (preferred)
    2) Leading emoji inside `title` (legacy)
    """
    explicit = (emoji or "").strip()
    if explicit:
        return explicit, (title or "").strip()

    title_emoji, title_text = split_leading_emoji_from_title(title)
    if title_emoji:
        return title_emoji, title_text

    return "", (title or "").strip()


def post_cover_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> cover_image_url (only when present)."""
    covers: dict[str, str] = {}
    for p in blog.list_posts():
        if p.cover_image_url:
            covers[p.slug] = p.cover_image_url
    return covers


def post_thumb_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> thumb_image_url (only when present)."""
    thumbs: dict[str, str] = {}
    for p in blog.list_posts():
        thumb = getattr(p, "thumb_image_url", None)
        if thumb:
            thumbs[p.slug] = thumb
    return thumbs


def post_blurb_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> blurb (only when present)."""
    blurbs: dict[str, str] = {}
    for p in blog.list_posts():
        blurb = getattr(p, "blurb", None)
        if blurb:
            blurbs[p.slug] = blurb
    return blurbs


def post_emoji_map() -> dict[str, str]:
    """Optional emoji thumbnails for posts without dedicated thumb/cover images."""
    return {
        "ai-standard": "🤖",
        "simple-hacking": "🛠️",
        "niche-tools": "🧰",
        "bots": "🛎️",
        "hardware-guides-are-accidental-bios": "🔧",
        "tiny-tools": "🧩",
        "the-led-problem-the-virpil-community-had": "💡",
        # 3D printing info has no dedicated icon asset - literal, not guessed
        "3D-printing-info": "🖨️",
        # Pre-existing emojis from old template hardcodes - restored, not invented
        "audiodeck": "🔊",
        "calendifier": "📅",
        "elevator": "🛗",
        "galacticunicorn": "🦄",
    }


def post_frontmatter_emoji_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> `emoji` declared in markdown frontmatter (if any)."""
    emojis: dict[str, str] = {}
    for p in blog.list_posts():
        emoji = (getattr(p, "emoji", None) or "").strip()
        if emoji:
            emojis[p.slug] = emoji
    return emojis


def post_summary_index(blog: BlogService) -> dict[str, object]:
    """Map post slug (lower) -> PostSummary."""
    out: dict[str, object] = {}
    for p in blog.list_posts():
        slug = (getattr(p, "slug", "") or "").strip().lower()
        if slug:
            out[slug] = p
    return out


def group_posts_by_cat(
    posts: list[dict[str, object]],
    *,
    view: str = "",
) -> list[dict[str, object]]:
    """Group a filtered post list by primary `cat:` tag for the pills index."""

    _CAT_TAG_PREFIX = "cat:"

    groups: dict[str, dict[str, object]] = {}

    for post in posts:
        tags = [str(t) for t in (post.get("tags") or [])]
        primary_cat: str | None = None
        for tag in tags:
            raw = (tag or "").strip()
            if raw.lower().startswith(_CAT_TAG_PREFIX):
                tail = raw.split(":", 1)[1].strip()
                if tail:  # pragma: no branch — real posts never emit a bare "cat:" tag
                    primary_cat = normalize_cat_label(tail)
                    break

        key = primary_cat.lower() if primary_cat else "\xff"
        if key not in groups:
            if primary_cat:
                groups[key] = {
                    "label": sidebar_label_with_emoji(primary_cat),
                    "cat": primary_cat,
                    "posts": [],
                }
            else:
                groups[key] = {
                    "label": "Other",
                    "cat": "",
                    "posts": [],
                }
        cast(list[dict[str, object]], groups[key]["posts"]).append(post)

    view_norm = (view or "").strip().lower()
    is_archive = view_norm == POSTS_VIEW_ARCHIVE
    is_writing = view_norm == POSTS_VIEW_WRITING

    def _archive_sort_key(item: tuple[str, dict[str, object]]) -> tuple[int, str]:
        key, _entry = item
        if key == "\xff":
            return (5, "")
        bucket = ARCHIVE_CAT_BUCKETS.get(key, 4)
        return (bucket, key)

    def _writing_sort_key(item: tuple[str, dict[str, object]]) -> tuple[int, str]:
        key, entry = item
        if key == "\xff":  # pragma: no cover — all writing posts carry a cat: tag
            return (2, "")
        if key == "blog":
            return (1, "")
        raw_label = str(entry.get("label") or entry.get("cat") or key)
        _emoji_part, text_part = split_leading_emoji_from_title(raw_label)
        sort_label = (text_part or raw_label).strip().lower()
        return (0, sort_label)

    def _default_sort_key(item: tuple[str, dict[str, object]]) -> tuple[int, str]:
        key, _entry = item
        if key == "\xff":  # pragma: no cover — all project posts carry a cat: tag
            return (2, "")
        return (0 if key == "leadership" else 1, key)

    if is_archive:
        sort_key = _archive_sort_key
    elif is_writing:
        sort_key = _writing_sort_key
    else:
        sort_key = _default_sort_key

    return [entry for _, entry in sorted(groups.items(), key=sort_key)]


def category_label_for_query(
    query: str,
    *,
    blog: BlogService | None = None,
    exclude_blog: bool = True,
) -> str | None:
    """Return the friendly sidebar label for an exact category query."""
    raw = (query or "").strip()
    if not raw:
        return None

    if blog is None:
        legacy: dict[str, str] = {
            "blog": "📝 Blog",
            "automation|monitoring|obs|script|ansible|terraform": "🤖 Automation",
            "machine learning|computer vision|ml|data": "🧠 Data / ML",
            "desktop|windows|app|pyside|qt|installer|clock|audio|streamdeck|"
            "stellody|trainer": "🖥️ Desktop Apps",
            "gaming|game|elite|dangerous|frontier|colonisation": "🎮 Gaming",
            "tool|tools|cli|utility|utilities|launcher|database|db": "🧰 Tools",
            "api|apis|fastapi|django|rest|web": "🌐 Web APIs",
        }
        return legacy.get(raw)

    for c in build_sidebar_categories(blog, exclude_blog=exclude_blog):
        if (str(c.get("query") or "")).strip().lower() == raw.lower():
            return cast(str | None, c.get("label"))
    return None


def is_project_post_by_tags(
    post_type: str,
    tags: list[str],
) -> bool:
    """Determine if a post is a project post.

    New model: structural frontmatter `post_type: project`.
    Transition fallback: infer from legacy portfolio categories.
    """
    if (post_type or "").strip().lower() == "project":
        return True
    cats = extract_category_queries_from_tags(tags)
    cats_lower = {
        (q.split(":", 1)[1].strip().lower() if ":" in q else q.strip().lower())
        for q in cats
    }
    return any(c in PROJECT_CATEGORY_LABELS for c in cats_lower)
