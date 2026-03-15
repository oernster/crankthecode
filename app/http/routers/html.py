from __future__ import annotations

import datetime as dt
import json
import unicodedata
from pathlib import Path
from typing import cast
from collections.abc import Mapping
from urllib.parse import quote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.http.deps import get_blog_service, get_templates
from app.http.seo import (
    DEFAULT_SITE_URL,
    absolute_url,
    build_meta_description,
    canonical_url_for_request,
    get_site_url,
    to_iso_datetime,
    to_iso_date,
)
from app.services.blog_service import BlogService
from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.domain.tags import extract_layer_slugs_from_tags
from app.domain.tags import humanize_layer_slug
from app.domain.tags import primary_layer_slug_from_tags
from app.domain.tags import normalize_layer_slug

router = APIRouter()

_CAT_TAG_PREFIX = "cat:"
_CAT_TAG_BLOG = "cat:blog"
_LAYER_TAG_PREFIX = "layer:"

# /posts filter model
_POSTS_VIEW_WRITING = "writing"
_POSTS_VIEW_PROJECTS = "projects"
_POSTS_VIEW_ARCHIVE = "archive"
_POSTS_ALLOWED_VIEWS = {
    _POSTS_VIEW_WRITING,
    _POSTS_VIEW_PROJECTS,
    _POSTS_VIEW_ARCHIVE,
}

# Portfolio / systems categories (conceptual: Projects)
_PROJECT_CATEGORY_LABELS = {
    "desktop apps",
    "tools",
    "gaming",
    "hardware",
    "web apis",
    "data / ml",
}

_TRUTHY_QUERY = {"1", "true", "yes", "y", "on"}
_FALSY_QUERY = {"0", "false", "no", "n", "off"}


def _sidebar_label_with_emoji(label: str) -> str:
    """Decorate known sidebar category labels with their legacy emoji.

    Category *queries* remain `cat:<Label>`; this is purely display polish.

    NOTE: Labels passed here are already normalized (Title Case) from
    `_normalize_cat_label()`.
    """

    key = (label or "").strip().lower()
    if not key:
        return label

    # Legacy sidebar labels (pre `cat:` automation).
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


_LEGACY_POST_REDIRECTS: dict[str, str] = {}


def _post_cover_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> cover_image_url (only when present)."""

    covers: dict[str, str] = {}
    for p in blog.list_posts():
        if p.cover_image_url:
            covers[p.slug] = p.cover_image_url
    return covers


def _post_thumb_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> thumb_image_url (only when present)."""

    thumbs: dict[str, str] = {}
    for p in blog.list_posts():
        thumb = getattr(p, "thumb_image_url", None)
        if thumb:
            thumbs[p.slug] = thumb
    return thumbs


def _post_blurb_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> blurb (only when present)."""

    blurbs: dict[str, str] = {}
    for p in blog.list_posts():
        blurb = getattr(p, "blurb", None)
        if blurb:
            blurbs[p.slug] = blurb
    return blurbs


def _split_leading_emoji_from_title(title: str) -> tuple[str | None, str]:
    """Split a leading emoji from a title.

    We use a heuristic rather than a full emoji grapheme parser.

    Rules:
    - If the first whitespace-delimited token looks like an emoji (Unicode symbol
      plus optional variation selector), treat it as the emoji.
    - Otherwise return (None, title).

    This is used purely for presentation (making the title emoji larger) while
    ensuring the emoji appears only once.
    """

    raw = (title or "").strip()
    if not raw:
        return None, ""

    token, sep, rest = raw.partition(" ")
    # Typical emoji tokens are short (1-3 codepoints). Allow a bit more for VS16.
    if not token or len(token) > 6:
        return None, raw

    def is_emojiish(ch: str) -> bool:
        if not ch or ord(ch) < 0x80:
            return False
        cat = unicodedata.category(ch)
        # Most emojis fall under "So" (Symbol, other). Some are followed by
        # variation selectors (Mn).
        return cat in {"So", "Sk"}

    has_symbol = any(is_emojiish(c) for c in token)
    if not has_symbol:
        return None, raw

    emoji = token
    title_text = rest.strip() if sep else ""
    return emoji, title_text or raw


def _display_title_parts(*, title: str, emoji: str | None) -> tuple[str, str]:
    """Return (emoji, title_text) for display without duplication.

    Preference order:
    1) Explicit frontmatter `emoji` (preferred)
    2) Leading emoji inside `title` (legacy)

    If we extract a leading emoji from the title, we return the remaining title
    text so templates can avoid showing the emoji twice.
    """

    explicit = (emoji or "").strip()
    if explicit:
        return explicit, (title or "").strip()

    title_emoji, title_text = _split_leading_emoji_from_title(title)
    if title_emoji:
        return title_emoji, title_text

    return "", (title or "").strip()


def _normalize_cat_label(raw_label: str) -> str:
    """Normalize `cat:` labels for display.

    Rules:
    - collapse whitespace
    - Title Case

    Note: this intentionally does *not* preserve acronyms (e.g. "APIs" -> "Apis")
    to match the requested behavior.
    """

    cleaned = " ".join((raw_label or "").strip().split())
    return cleaned.title()


def _humanize_layer_slug(layer_slug: str) -> str:
    """Backwards-compatible wrapper.

    Prefer [`humanize_layer_slug()`](app/domain/tags.py:1).
    """

    return humanize_layer_slug(layer_slug)


def _normalize_layer_slug(raw_slug: str) -> str:
    """Backwards-compatible wrapper.

    Prefer [`normalize_layer_slug()`](app/domain/tags.py:1).
    """

    return normalize_layer_slug(raw_slug)


def _extract_category_queries_from_tags(tags: list[str]) -> set[str]:
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
            # Guard against tags like "cat:".
            continue
        label = _normalize_cat_label(tail)
        out.add(f"cat:{label}".strip())
    return out


def _extract_layer_slugs_from_tags(tags: list[str]) -> set[str]:
    """Backwards-compatible wrapper.

    Prefer [`extract_layer_slugs_from_tags()`](app/domain/tags.py:1).
    """

    # Keep semantics: only layer tags.
    return extract_layer_slugs_from_tags(tags)


def _is_blog_post_by_cat(tags: list[str]) -> bool:
    return any((t or "").strip().lower() == _CAT_TAG_BLOG for t in (tags or []))


def _posts_href(
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


def _posts_view_href(
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


def _posts_base_href(*, view: str | None = None) -> str:
    """Canonical breadcrumb href for the Posts listing.

    Keep breadcrumbs deterministic by including the selected `view` when present.
    """

    view_norm = _normalize_posts_view(view)
    if not view_norm:
        return "/posts"
    return f"/posts?view={quote(view_norm, safe='')}"


def _normalize_posts_view(raw: str | None) -> str:
    view = (raw or "").strip().lower()
    return view if view in _POSTS_ALLOWED_VIEWS else ""


def _posts_view_from_legacy_exclude_blog(raw: str | None) -> str | None:
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
        return _POSTS_VIEW_PROJECTS
    if val in _FALSY_QUERY:
        return _POSTS_VIEW_ARCHIVE
    return None


def _sidebar_categories(
    blog: BlogService, *, exclude_blog: bool
) -> list[dict[str, object]]:
    """Build sidebar categories from explicit `cat:` tags and nested `layer:` tags.

    URL scheme:
    - Category: `/posts?cat=<Cat>`
    - Layer (subcategory): `/posts?cat=<Cat>&layer=<LayerSlug>`

    `exclude_blog` behaviour:
    - When blog posts are included (`exclude_blog=False`), links preserve that
      choice by including `exclude_blog=0`.
    - When blog posts are excluded (`exclude_blog=True`), the Blog category links
      *force include* by setting `exclude_blog=0`.
    """

    # category_key -> entry
    cats: dict[str, dict[str, object]] = {}

    for p in blog.list_posts():
        tags = [str(t) for t in (p.tags or [])]
        cat_queries = _extract_category_queries_from_tags(tags)
        if not cat_queries:
            continue

        layers = _extract_layer_slugs_from_tags(tags)
        for q in cat_queries:
            cat_label = q.split(":", 1)[1].strip() if ":" in q else q
            cat_label_norm = _normalize_cat_label(cat_label)

            key = cat_label_norm.lower()
            entry = cats.get(key)
            if entry is None:
                entry = {
                    "cat": cat_label_norm,
                    "query": f"cat:{cat_label_norm}",
                    "label": _sidebar_label_with_emoji(cat_label_norm),
                    "layers_map": {},
                }
                cats[key] = entry

            layers_map = cast(dict[str, dict[str, str]], entry["layers_map"])
            for layer_slug in layers:
                layers_map.setdefault(
                    layer_slug,
                    {
                        "layer": layer_slug,
                        "label": _humanize_layer_slug(layer_slug),
                    },
                )

    def category_sort_key(entry: dict[str, object]) -> tuple[int, str]:
        """Sort categories for the sidebar.

        Requirements:
        - Pin Decision Architecture (internally `cat:Leadership`) to the top.
        - Sort everything else alphabetically.
        """

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
                "href": _posts_href(
                    query=None,
                    cat=cat_label_norm,
                    layer=None,
                    exclude_blog=href_exclude_blog,
                ),
                "layers": [
                    {
                        "layer": layer_entry["layer"],
                        "label": layer_entry["label"],
                        "href": _posts_href(
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


def _homepage_leadership_items(blog: BlogService) -> list[dict[str, object]]:
    """Homepage Leadership content grouped by `layer:`.

    Grouping rules:
    - include any post with an *exact* `cat:Leadership` tag (case-insensitive)
    - if the post has one or more `layer:` tags, group under each layer
      (duplicates are de-duped)
    - if it has no `layer:`, group under "General"
    """

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
        layer_slugs = sorted(_extract_layer_slugs_from_tags(tags))
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
        return _humanize_layer_slug(slug).lower()

    out: list[dict[str, object]] = []
    for layer_slug in sorted(layer_to_items.keys(), key=layer_sort_key):
        out.append(
            {
                "layer": layer_slug,
                "label": _humanize_layer_slug(layer_slug) if layer_slug else "General",
                # NOTE: avoid the key name `items` because Jinja may resolve
                # `g.items` to the dict method instead of the key.
                "posts": layer_to_items[layer_slug],
            }
        )

    return out


def _post_emoji_map() -> dict[str, str]:
    """Optional emoji thumbnails for posts without dedicated thumb/cover images."""

    return {
        # Backlog items (no cover thumbs)
        "ai-standard": "🤖",
        "simple-hacking": "🛠️",
        "niche-tools": "🧰",
        "bots": "🛎️",
        "hardware-guides-are-accidental-bios": "🔧",
        "tiny-tools": "🧩",
        "the-led-problem-the-virpil-community-had": "💡",
    }


def _post_frontmatter_emoji_index(blog: BlogService) -> dict[str, str]:
    """Map post slug -> `emoji` declared in markdown frontmatter (if any)."""

    emojis: dict[str, str] = {}
    for p in blog.list_posts():
        emoji = (getattr(p, "emoji", None) or "").strip()
        if emoji:
            emojis[p.slug] = emoji
    return emojis


def _base_context(request: Request) -> dict:
    site_url = get_site_url(request)
    exclude_blog_raw = (request.query_params.get("exclude_blog") or "").strip().lower()
    # Default to hiding blog entries from listings unless explicitly included.
    exclude_blog = (
        True
        if exclude_blog_raw == ""
        else exclude_blog_raw in {"1", "true", "yes", "y", "on"}
    )
    return {
        "request": request,
        "site_url": site_url,
        "current_year": dt.datetime.now(dt.timezone.utc).year,
        # Optional override for `<title>` in `base.html`.
        "page_title": None,
        "site_name": "Crank The Code",
        "robots_meta": "index,follow",
        "canonical_url": canonical_url_for_request(request, site_url=site_url),
        "og_title": "Crank The Code",
        "og_description": None,
        "og_type": "website",
        "og_image_url": absolute_url(site_url, "/static/images/me.jpg"),
        "jsonld_extra_json": None,
        "meta_description": (
            "Crank The Code - Python engineering blog and technical write-ups by "
            "Oliver Ernster."
        ),
        # Filled by routes (requires BlogService).
        "sidebar_categories": [],
        "current_q": (request.query_params.get("q") or "").strip(),
        "current_cat": (request.query_params.get("cat") or "").strip(),
        "current_layer": (request.query_params.get("layer") or "").strip(),
        "exclude_blog": exclude_blog,
        "breadcrumb_items": [
            {"label": "Home", "href": "/"},
        ],
    }


def _person_jsonld_oliver_ernster(*, site_url: str) -> dict[str, object]:
    """Primary `Person` entity for Oliver Ernster.

    This is used on both the homepage and the About page to strengthen the
    entity association between the person and the domain.
    """

    home = absolute_url(site_url, "/")
    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "@id": f"{home}#oliver-ernster",
        "name": "Oliver Ernster",
        "url": home,
        "jobTitle": "Senior Python Developer",
        "description": (
            "Senior Python Developer and CTO-level technologist focused on decision "
            "systems, authority alignment and backend architecture."
        ),
        "sameAs": [
            "https://github.com/oernster",
        ],
        "knowsAbout": [
            "Python",
            "FastAPI",
            "AWS",
            "Decision Systems",
            "Backend Architecture",
            "Authority Alignment",
            "Organisational Design",
        ],
    }


def _is_leadership_post(tags: list[str]) -> bool:
    """Return True if tags include the `cat:Leadership` category."""

    return any((t or "").strip().lower() == "cat:leadership" for t in (tags or []))


def _topic_descriptions() -> dict[str, str]:
    """Short, calm topic blurbs keyed by normalized `layer:` slug."""

    return {
        "decision-systems": "Decision ownership, option space, and the mechanics of stable decisions at scale.",
        "cto-operating-model": "Authority, escalation, and operating rhythms that keep execution coherent.",
        "organisational-structure": "Roles, boundaries, and structure as the substrate for durable delivery.",
        "structural-design": "Models and primitives for designing organisations that compound rather than fragment.",
        "architecture": "Architecture as boundary design: where constraints live, and how systems stay legible.",
    }


def _leadership_topic_hubs(blog: BlogService) -> list[dict[str, object]]:
    """Derive stable topic hubs from existing `cat:Leadership` + `layer:` tags."""

    # layer_slug -> (latest_date_str, count)
    layer_counts: dict[str, int] = {}
    for p in blog.list_posts():
        tags = [str(t) for t in (p.tags or [])]
        if not _is_leadership_post(tags):
            continue
        layer_slugs = sorted(extract_layer_slugs_from_tags(tags))
        if not layer_slugs:
            layer_slugs = [""]
        for layer_slug in layer_slugs:
            layer_counts[layer_slug] = layer_counts.get(layer_slug, 0) + 1

    # Keep ordering stable and intentional where possible; fall back to label sort.
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

    descriptions = _topic_descriptions()
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

    # Ensure we don't accidentally expose an empty-slug URL; normalize it to /topics/general.
    for h in hubs:
        if h.get("layer") == "":
            h["layer"] = "general"
    return hubs


def _topic_layer_slug_for_route(raw: str) -> str:
    """Normalize topic route param.

    - `general` is a stable alias for posts with no `layer:`.
    - Everything else uses the existing layer normalizer.
    """

    cleaned = (raw or "").strip().lower()
    if cleaned in {"", "general"}:
        return "general"
    return normalize_layer_slug(cleaned)


def _topic_posts_for_layer(blog: BlogService, *, layer_slug: str) -> list[dict[str, object]]:
    """Return leadership posts for a given normalized topic `layer_slug`."""

    out: list[dict[str, object]] = []
    for p in blog.list_posts():
        tags = [str(t) for t in (p.tags or [])]
        if not _is_leadership_post(tags):
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
                "primary_layer": primary,
            }
        )

    out.sort(key=lambda i: str(i.get("date", "")), reverse=True)
    return out


def _category_label_for_query(
    query: str,
    *,
    blog: BlogService | None = None,
    exclude_blog: bool = True,
) -> str | None:
    """Return the friendly sidebar label for an exact category query.

    Backwards-compatible behavior:
    - When called without `blog`, return the legacy labels for the old hardcoded
      query strings. This keeps existing tests and call sites stable.
    """

    raw = (query or "").strip()
    if not raw:
        return None

    if blog is None:
        legacy: dict[str, str] = {
            "blog": "📝 Blog",
            "automation|monitoring|obs|script|ansible|terraform": "🤖 Automation",
            "machine learning|computer vision|ml|data": "🧠 Data / ML",
            # Keep this on a separate line for Flake8's 88-char limit.
            "desktop|windows|app|pyside|qt|installer|clock|audio|streamdeck|"
            "stellody|trainer": "🖥️ Desktop Apps",
            "gaming|game|elite|dangerous|frontier|colonisation": "🎮 Gaming",
            "tool|tools|cli|utility|utilities|launcher|database|db": "🧰 Tools",
            "api|apis|fastapi|django|rest|web": "🌐 Web APIs",
        }
        return legacy.get(raw)

    for c in _sidebar_categories(blog, exclude_blog=exclude_blog):
        if (str(c.get("query") or "")).strip().lower() == raw.lower():
            return cast(str | None, c.get("label"))
    return None


def _load_about_html() -> str:
    """Render the About me markdown into HTML.

    This is intentionally loaded directly from the posts directory so it can be
    used on a dedicated page without appearing in the main post index or RSS.
    """

    try:
        repo = FilesystemPostsRepository(posts_dir=Path("posts"))
        about_post = repo.get_post("about-me")
        if about_post is None:
            return ""
        return PythonMarkdownRenderer().render(about_post.content_markdown)
    except Exception:
        # Fail open: pages should still render if about content can't be loaded.
        return ""


def _load_portfolio_post() -> object | None:
    """Load the `posts/portfolio.md` page content (markdown + frontmatter).

    This is a *page* (served at `/portfolio`), not a regular post listing item.
    We still store the copy in `posts/` to keep content editable in markdown.
    """

    try:
        repo = FilesystemPostsRepository(posts_dir=Path("posts"))
        return repo.get_post("portfolio")
    except Exception:
        return None


def _render_portfolio_intro_html() -> str:
    post = _load_portfolio_post()
    if post is None:
        return ""
    try:
        return PythonMarkdownRenderer().render(getattr(post, "content_markdown", "") or "")
    except Exception:
        return ""


def _post_summary_index(blog: BlogService) -> dict[str, object]:
    """Map post slug (lower) -> PostSummary."""

    out: dict[str, object] = {}
    for p in blog.list_posts():
        slug = (getattr(p, "slug", "") or "").strip().lower()
        if slug:
            out[slug] = p
    return out


def _curated_portfolio_entries_from_slugs(
    *,
    slugs: list[str],
    index: dict[str, object],
    hidden: set[str],
    emoji_map: dict[str, str],
    emoji_index: dict[str, str],
) -> list[dict[str, object]]:
    """Convert a curated list of slugs into Portfolio entries.

    This helper is intentionally defensive:
    - ignores empty slugs
    - ignores special/hidden slugs
    - ignores missing slugs not present in the blog index
    """

    entries: list[dict[str, object]] = []
    for raw in slugs:
        key = (str(raw or "")).strip().lower()
        if not key or key in hidden:
            continue

        summary = index.get(key)
        if summary is None:
            continue

        entries.append(
            _portfolio_item_from_summary(
                summary=summary,
                emoji_map=emoji_map,
                frontmatter_emoji_index=emoji_index,
            )
        )

    return entries


def _has_cat_tag(tags: list[str], cat_label: str) -> bool:
    target = f"cat:{(cat_label or '').strip().lower()}"
    return any((t or "").strip().lower() == target for t in (tags or []))


def _has_any_cat_tag(tags: list[str], cat_labels: list[str]) -> bool:
    return any(_has_cat_tag(tags, lbl) for lbl in (cat_labels or []))


def _portfolio_item_from_summary(
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


def _portfolio_flagship_entries(blog: BlogService) -> list[dict[str, object]]:
    """Return portfolio entries for any project(s) with `role: flagship`.

    Rules:
    - select posts where `post_type == 'project'` and `role == 'flagship'`
    - preserve chronological ordering (newest-first), matching `blog.list_posts()`
    """

    emoji_map = _post_emoji_map()
    emoji_index = _post_frontmatter_emoji_index(blog)

    out: list[dict[str, object]] = []
    for p in blog.list_posts():
        post_type = str(getattr(p, "post_type", "") or "").strip().lower()
        if post_type != "project":
            continue
        role = str(getattr(p, "role", "") or "").strip().lower()
        if role != "flagship":
            continue
        out.append(
            _portfolio_item_from_summary(
                summary=p,
                emoji_map=emoji_map,
                frontmatter_emoji_index=emoji_index,
            )
        )
    return out


def _portfolio_groups(blog: BlogService) -> list[dict[str, object]]:
    """Build the curated Portfolio page groups.

    Rules:
    - Desktop Applications: curated.
    - Hardware / Embedded: any `cat:Hardware`, with Galactic Unicorn pinned first.
    - Tools: any `cat:Tools`.

    Categories remain usable via `/posts?cat=<Label>` but do not dominate nav.
    """

    emoji_map = _post_emoji_map()
    emoji_index = _post_frontmatter_emoji_index(blog)
    index = _post_summary_index(blog)

    hidden = {"about-me", "start-here", "portfolio"}

    # Flagship projects are rendered separately (at the top of the page).
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

    desktop_items = _curated_portfolio_entries_from_slugs(
        slugs=["fancy-clock", "calendifier", "elevator"],
        index=index,
        hidden=hidden,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )

    # Avoid duplicates across groups (curated entries should not reappear in
    # category-derived buckets).
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
        if _has_cat_tag(tags, "Desktop Apps"):
            desktop_summaries.append(p)
        # Note: historical casing drift: some posts are tagged `cat:Data / Ml`.
        if _has_any_cat_tag(tags, ["Data / Ml", "Data / ML"]):
            data_summaries.append(p)
        if _has_cat_tag(tags, "Gaming"):
            gaming_summaries.append(p)
        if _has_cat_tag(tags, "Hardware"):
            hardware_summaries.append(p)
        if _has_cat_tag(tags, "Tools"):
            tools_summaries.append(p)
        if _has_any_cat_tag(tags, ["Web Apis", "Web APIs"]):
            webapi_summaries.append(p)

    def date_key(p: object) -> str:
        # `PostSummary.date` is sortable as a string (YYYY-MM-DD HH:MM).
        return str(getattr(p, "date", "") or "")

    data_summaries.sort(key=date_key, reverse=True)
    desktop_summaries.sort(key=date_key, reverse=True)
    gaming_summaries.sort(key=date_key, reverse=True)
    hardware_summaries.sort(key=date_key, reverse=True)
    tools_summaries.sort(key=date_key, reverse=True)
    webapi_summaries.sort(key=date_key, reverse=True)

    # Pin Galactic Unicorn first (if present) so the embedded/projects anchor is obvious.
    pinned_hardware = []
    rest_hardware = []
    for p in hardware_summaries:
        if str(getattr(p, "slug", "") or "").strip().lower() == "galacticunicorn":
            pinned_hardware.append(p)
        else:
            rest_hardware.append(p)
    hardware_items = [
        _portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in (pinned_hardware + rest_hardware)
    ]

    # Tools: category-derived plus a pinned supporting tool.
    pinned_tools = _curated_portfolio_entries_from_slugs(
        slugs=["audiodeck"],
        index=index,
        hidden=hidden,
        emoji_map=emoji_map,
        emoji_index=emoji_index,
    )
    tools_items = pinned_tools + [
        _portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in tools_summaries
    ]

    # De-dupe tools (AudioDeck could be tagged as Tools in future).
    seen: set[str] = set()
    tools_items_deduped: list[dict[str, object]] = []
    for it in tools_items:
        slug = str(it.get("slug") or "").strip().lower()
        if not slug or slug in seen:
            continue
        seen.add(slug)
        tools_items_deduped.append(it)

    # Old category resurfacing (portfolio-only): the category sets that used to
    # live in the global sidebar.
    desktop_items_auto = [
        _portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in desktop_summaries
        if str(getattr(p, "slug", "") or "").strip().lower() != "audiodeck"
    ]
    data_items = [
        _portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in data_summaries
    ]
    gaming_items = [
        _portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in gaming_summaries
    ]
    webapi_items = [
        _portfolio_item_from_summary(
            summary=p,
            emoji_map=emoji_map,
            frontmatter_emoji_index=emoji_index,
        )
        for p in webapi_summaries
    ]

    desktop_all = [*desktop_items, *desktop_items_auto]

    return [
        {
            "label": "Desktop Applications",
            "description": "Independent desktop systems (UI + local operations).",
            "entries": desktop_all,
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
            "label": "Tools",
            "description": "Supporting tooling and utilities.",
            "entries": tools_items_deduped,
            "more_href": "/posts?cat=Tools",
        },
    ]


@router.get("/", response_class=HTMLResponse)
async def homepage(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )
    cover_index = _post_cover_index(blog)
    thumb_index = _post_thumb_index(blog)
    blurb_index = _post_blurb_index(blog)
    emoji_index = _post_frontmatter_emoji_index(blog)

    homepage_meta = {
        "is_homepage": True,
        "page_title": (
            "Oliver Ernster - Senior Python Developer & Decision Systems Technologist"
        ),
        "og_title": "Oliver Ernster | Crank The Code",
        "og_description": (
            "Oliver Ernster is a Senior Python Developer and CTO-level technologist "
            "writing about decision systems, authority alignment and backend "
            "architecture."
        ),
        "meta_description": (
            "Oliver Ernster is a Senior Python Developer and CTO-level technologist "
            "writing about decision systems, authority alignment and backend "
            "architecture."
        ),
    }

    ctx.update(
        {
            # NOTE: Homepage meta is applied at the end of this route to prevent
            # accidental overrides.
            "breadcrumb_items": [{"label": "Home", "href": "/"}],
            "homepage_projects": {
                "leadership": _homepage_leadership_items(blog),
            },
            "homepage_cover_index": cover_index,
            "homepage_thumb_index": thumb_index,
            "homepage_blurb_index": blurb_index,
            "homepage_emoji_index": emoji_index,
        }
    )

    # Entity SEO: WebSite -> Person graph linking.
    # Keep homepage structured data stable and explicitly linked via @id.
    site_url = get_site_url(request)
    home = absolute_url(site_url, "/")
    person_jsonld = _person_jsonld_oliver_ernster(site_url=site_url)

    homepage_jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{home}#website",
                "name": "Crank The Code",
                "url": home,
                "author": {"@id": f"{home}#oliver-ernster"},
                # Explicitly define the site's main entity to strengthen the
                # WebSite -> Person association for crawlers and AI systems.
                "mainEntity": {"@id": f"{home}#oliver-ernster"},
            },
            person_jsonld,
        ],
    }
    ctx["jsonld_json"] = json.dumps(
        homepage_jsonld, ensure_ascii=False, separators=(",", ":")
    )
    # Ensure we only emit a single JSON-LD script block on the homepage.
    ctx["jsonld_extra_json"] = None

    # Critical requirement: the homepage must always prioritize Oliver Ernster
    # in title and OG metadata and must not fall back to the generic site-wide
    # defaults from `_base_context()`.
    ctx.update(homepage_meta)

    return templates.TemplateResponse(request, "index.html", ctx)


@router.get("/posts", response_class=HTMLResponse)
async def posts_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    emoji_map = _post_emoji_map()
    posts = [
        (
            lambda _p: (
                {
                    "slug": _p.slug,
                    "title": _p.title,
                    "title_text": _display_title_parts(
                        title=_p.title,
                        emoji=(
                            getattr(_p, "emoji", None) or emoji_map.get(_p.slug, "")
                        ),
                    )[1],
                    "date": _p.date,
                    "tags": list(_p.tags),
                    "post_type": getattr(_p, "post_type", None),
                    "blurb": getattr(_p, "blurb", None),
                    "one_liner": getattr(_p, "one_liner", None),
                    "cover_image_url": _p.cover_image_url,
                    "thumb_image_url": getattr(_p, "thumb_image_url", None),
                    "emoji": _display_title_parts(
                        title=_p.title,
                        emoji=(
                            getattr(_p, "emoji", None) or emoji_map.get(_p.slug, "")
                        ),
                    )[0],
                    # Keep links in summaries clickable.
                    "summary_html": _p.summary_html,
                }
            )
        )(p)
        for p in blog.list_posts()
    ]

    # Special pages:
    # - “About me” is rendered on a dedicated `/about` page
    # - “Start Here” is promoted via the header buttons
    # These should not appear in any post listing (including “All posts (exc. Blog)”).
    hidden_slugs = {"about-me", "about", "start-here", "portfolio"}
    posts = [
        p for p in posts if str(p.get("slug", "")).strip().lower() not in hidden_slugs
    ]
    ctx = _base_context(request)
    current_q = (ctx.get("current_q", "") or "").strip()
    current_cat_raw = (ctx.get("current_cat", "") or "").strip()
    current_layer_raw = (ctx.get("current_layer", "") or "").strip()

    # Sidebar categories are tag-driven (legacy). The global sidebar is now
    # conceptual and template-driven, but we keep this populated for backwards
    # compatibility with any templates that still reference it.
    ctx["sidebar_categories"] = _sidebar_categories(blog, exclude_blog=bool(ctx.get("exclude_blog")))

    # Support legacy deep-links: `/posts?q=cat:<Label>` should behave like
    # `/posts?cat=<Label>`.
    cat_label: str | None = None
    if current_cat_raw:
        cat_label = _normalize_cat_label(current_cat_raw)
    elif (
        current_q.lower().startswith(_CAT_TAG_PREFIX)
        and current_q.strip().lower() != _CAT_TAG_PREFIX
    ):
        tail = current_q.split(":", 1)[1].strip()
        cat_label = _normalize_cat_label(tail) if tail else None

    layer_slug: str | None = None
    if current_layer_raw:
        layer_slug = _normalize_layer_slug(current_layer_raw)

    # Expose normalized values for templates (active states).
    ctx["current_cat"] = cat_label or ""
    ctx["current_layer"] = layer_slug or ""

    # Determine the content-type view.
    # Priority:
    # 1) explicit `view=`
    # 2) legacy `exclude_blog=` mapping
    # 3) sensible default based on category deep-link (transition: project categories)
    view_norm = _normalize_posts_view(request.query_params.get("view"))
    legacy_view = (
        None
        if view_norm
        else _posts_view_from_legacy_exclude_blog(request.query_params.get("exclude_blog"))
    )

    cat_norm = (cat_label or "").strip().lower()
    default_view = (
        _POSTS_VIEW_PROJECTS if cat_norm in _PROJECT_CATEGORY_LABELS else _POSTS_VIEW_WRITING
    )
    current_view = view_norm or legacy_view or default_view
    ctx["current_view"] = current_view

    def _is_project_post(post: Mapping[str, object]) -> bool:
        # New model: structural frontmatter `type: project`.
        post_type = str(post.get("post_type") or "").strip().lower()
        if post_type == "project":
            return True

        # Transition fallback: infer projects from legacy portfolio categories.
        tags_obj = post.get("tags") or []
        tags = [str(t) for t in cast(list[object], tags_obj)]
        cats = _extract_category_queries_from_tags(tags)
        cats_lower = {
            (q.split(":", 1)[1].strip().lower() if ":" in q else q.strip().lower())
            for q in cats
        }
        return any(c in _PROJECT_CATEGORY_LABELS for c in cats_lower)

    # Content-type filtering (primary)
    if current_view == _POSTS_VIEW_WRITING:
        # Writing = everything except portfolio/system categories.
        # Uncategorized posts are treated as writing by default.
        posts = [p for p in posts if not _is_project_post(p)]
    elif current_view == _POSTS_VIEW_PROJECTS:
        posts = [p for p in posts if _is_project_post(p)]
    elif current_view == _POSTS_VIEW_ARCHIVE:
        posts = posts
    else:  # pragma: no cover
        # Defensive fallback; should be unreachable due to normalization.
        posts = [p for p in posts if not _is_project_post(p)]

    # Server-side filtering for category + layer (AND semantics).
    if cat_label:
        # Use the same normalization logic as the sidebar builder so tags like
        # `cat:leadership` still match `cat=Leadership`.
        cat_tag_norm = f"cat:{_normalize_cat_label(cat_label)}".strip().lower()
        posts = [
            p
            for p in posts
            if any(
                (q or "").strip().lower() == cat_tag_norm
                for q in _extract_category_queries_from_tags(
                    [str(t) for t in (p.get("tags") or [])]
                )
            )
        ]

    if layer_slug:
        layer_tag_norm = f"layer:{_normalize_layer_slug(layer_slug)}".strip().lower()
        posts = [
            p
            for p in posts
            if any(
                f"layer:{s}".strip().lower() == layer_tag_norm
                for s in _extract_layer_slugs_from_tags(
                    [str(t) for t in (p.get("tags") or [])]
                )
            )
        ]

    category_label = None
    if cat_label:
        category_label = _sidebar_label_with_emoji(cat_label)
    else:
        category_label = _category_label_for_query(current_q, blog=blog, exclude_blog=False)

    layer_label = _humanize_layer_slug(layer_slug) if layer_slug else None

    # SEO: category/layer deep-links should have distinct titles/descriptions.
    page_title = "Posts | Crank The Code"
    og_title = "Posts | Crank The Code"
    og_description = "Browse all Crank The Code posts and project write-ups."
    meta_description = "Browse all Crank The Code posts and project write-ups."
    if cat_label:
        cat_display = (category_label or cat_label).strip()
        _, cat_text = _split_leading_emoji_from_title(cat_display)
        cat_text = (cat_text or cat_display).strip()
        if layer_label:
            page_title = f"{layer_label} | {cat_text} | Posts | Crank The Code"
            og_title = page_title
            og_description = (
                f"Browse posts in {layer_label} ({cat_text}) on Crank The Code."
            )
            meta_description = og_description
        elif cat_text:
            page_title = f"{cat_text} | Posts | Crank The Code"
            og_title = page_title
            og_description = f"Browse posts in {cat_text} on Crank The Code."
            meta_description = og_description
        else:
            # Category label can be entirely empty/emoji-only.
            # Keep the generic Posts page metadata.
            meta_description = meta_description  # pragma: no cover

    writing_href = _posts_view_href(
        view=_POSTS_VIEW_WRITING,
        query=current_q or None,
        cat=cat_label,
        layer=layer_slug,
    )
    projects_href = _posts_view_href(
        view=_POSTS_VIEW_PROJECTS,
        query=current_q or None,
        cat=cat_label,
        layer=layer_slug,
    )
    archive_href = _posts_view_href(
        view=_POSTS_VIEW_ARCHIVE,
        query=current_q or None,
        cat=cat_label,
        layer=layer_slug,
    )

    filtered_href = _posts_view_href(
        view=current_view,
        query=None,
        cat=cat_label,
        layer=layer_slug,
    )
    ctx.update(
        {
            "posts": posts,
            "is_homepage": False,
            "page_title": page_title,
            "og_title": og_title,
            "og_description": og_description,
            "meta_description": meta_description,
            "writing_href": writing_href,
            "projects_href": projects_href,
            "archive_href": archive_href,
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Posts", "href": _posts_base_href(view=current_view)},
                *(
                    [
                        {
                            "label": category_label or cat_label,
                            "href": _posts_href(
                                query=None,
                                cat=cat_label,
                                layer=None,
                                exclude_blog=None,
                            ),
                        }
                    ]
                    if cat_label
                    else []
                ),
                *(
                    [
                        {
                            "label": layer_label,
                            "href": filtered_href,
                        }
                    ]
                    if (cat_label and layer_label)
                    else []
                ),
            ],
        }
    )

    resp = templates.TemplateResponse(request, "posts.html", ctx)
    # Dev-only safety: clear browser HTTP cache to avoid sticky cached redirects
    # while iterating on legacy slug behavior.
    hostname = (request.url.hostname or "").strip().lower()
    if hostname in {"127.0.0.1", "localhost"}:
        resp.headers["Clear-Site-Data"] = '"cache"'
    return resp


@router.get("/about", response_class=HTMLResponse)
async def about_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    site_url = get_site_url(request)
    canonical = absolute_url(site_url, "/about")
    home = absolute_url(site_url, "/")

    # Strong author page: WebPage + explicit about-linking to the Person entity.
    about_page_jsonld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": f"{canonical}#webpage",
        "url": canonical,
        "name": "About Oliver Ernster",
        "about": {"@id": f"{home}#oliver-ernster"},
        "isPartOf": {"@id": f"{home}#website"},
    }

    breadcrumb_jsonld = {
        "@context": "https://schema.org",
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
                "name": "About",
                "item": canonical,
            },
        ],
    }

    ctx.update(
        {
            "about_html": _load_about_html(),
            "topic_hubs": _leadership_topic_hubs(blog),
            "is_homepage": False,
            "page_title": "About Oliver Ernster | Senior Python Developer",
            "og_title": "About Oliver Ernster",
            "og_description": (
                "About Oliver Ernster, Senior Python Developer and CTO-level "
                "technologist."
            ),
            "meta_description": (
                "About Oliver Ernster, Senior Python Developer and CTO-level "
                "technologist."
            ),
            "back_link_href": "/",
            "back_link_label": "← Back to posts",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "About", "href": "/about"},
            ],
        }
    )

    ctx["jsonld_json"] = json.dumps(
        about_page_jsonld, ensure_ascii=False, separators=(",", ":")
    )
    # Emit Person + Breadcrumb as a second JSON-LD block.
    ctx["jsonld_extra_json"] = json.dumps(
        {
            "@context": "https://schema.org",
            "@graph": [
                _person_jsonld_oliver_ernster(site_url=site_url),
                breadcrumb_jsonld,
            ],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return templates.TemplateResponse(request, "about.html", ctx)


@router.get("/portfolio", response_class=HTMLResponse)
async def portfolio_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    md = _load_portfolio_post()
    title = str(getattr(md, "title", "Portfolio") if md is not None else "Portfolio")
    emoji = str(getattr(md, "emoji", "") if md is not None else "").strip()
    one_liner = str(getattr(md, "one_liner", "") if md is not None else "").strip()
    intro_html = _render_portfolio_intro_html()

    # SEO: include the target phrase explicitly.
    meta_description = (
        one_liner
        or "Independent software systems and engineering experiments built outside commercial environments."
    )
    if "software systems and engineering experiments" not in meta_description.lower():
        meta_description = (
            meta_description.strip().removesuffix(".")
            + ". Software systems and engineering experiments."
        )

    ctx.update(
        {
            "is_homepage": False,
            "page_title": f"{title} | Crank The Code",
            "og_title": f"{title} | Crank The Code",
            "og_description": meta_description,
            "meta_description": meta_description,
            "canonical_url": absolute_url(get_site_url(request), "/portfolio"),
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Portfolio", "href": "/portfolio"},
            ],
            "page_heading": title,
            "page_emoji": emoji or "🧩",
            "page_intro_html": intro_html,
            "flagship_entries": _portfolio_flagship_entries(blog),
            "portfolio_groups": _portfolio_groups(blog),
        }
    )

    return templates.TemplateResponse(request, "portfolio.html", ctx)


@router.get("/about/oliver-ernster", include_in_schema=False)
async def about_oliver_ernster_redirect(request: Request):
    """Alias route to strengthen entity discoverability.

    Canonical remains `/about`.
    """

    return RedirectResponse(url="/about", status_code=301)


@router.get("/topics", response_class=HTMLResponse)
async def topics_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    hubs = _leadership_topic_hubs(blog)

    site_url = get_site_url(request)
    canonical = absolute_url(site_url, "/topics")
    home = absolute_url(site_url, "/")

    item_list = {
        "@type": "ItemList",
        "itemListOrder": "http://schema.org/ItemListOrderAscending",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": str(h.get("label") or ""),
                "item": absolute_url(site_url, str(h.get("href") or "/topics")),
            }
            for idx, h in enumerate(hubs)
        ],
    }

    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": f"{canonical}#collection",
        "url": canonical,
        "name": "Topics",
        "about": {"@id": f"{home}#oliver-ernster"},
        "isPartOf": {"@id": f"{home}#website"},
        "mainEntity": item_list,
    }

    breadcrumb_jsonld = {
        "@context": "https://schema.org",
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
                "name": "Topics",
                "item": canonical,
            },
        ],
    }

    ctx.update(
        {
            "is_homepage": False,
            "page_title": "Topics | Crank The Code",
            "og_title": "Topics | Crank The Code",
            "og_description": "Topic hubs for the Decision Architecture / Leadership layer.",
            "meta_description": "Topic hubs for the Decision Architecture / Leadership layer.",
            "topic_hubs": hubs,
            "jsonld_json": json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")),
            "jsonld_extra_json": json.dumps(
                breadcrumb_jsonld, ensure_ascii=False, separators=(",", ":")
            ),
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Topics", "href": "/topics"},
            ],
        }
    )
    return templates.TemplateResponse(request, "topics_index.html", ctx)


@router.get("/topics/{layer_slug}", response_class=HTMLResponse)
async def topic_hub_page(
    request: Request,
    layer_slug: str,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    topic_slug = _topic_layer_slug_for_route(layer_slug)
    hubs = _leadership_topic_hubs(blog)

    # Find label/description from derived hubs (source of truth).
    hub = next((h for h in hubs if (h.get("layer") or "") == topic_slug), None)
    topic_label = (
        str(hub.get("label"))
        if hub is not None
        else (humanize_layer_slug(topic_slug) if topic_slug != "general" else "General")
    )
    topic_description = str(hub.get("description") or "") if hub is not None else ""

    posts = _topic_posts_for_layer(blog, layer_slug=topic_slug)

    site_url = get_site_url(request)
    canonical_path = f"/topics/{topic_slug}"
    canonical = absolute_url(site_url, canonical_path)
    home = absolute_url(site_url, "/")

    item_list = {
        "@type": "ItemList",
        "itemListOrder": "http://schema.org/ItemListOrderDescending",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": p.get("title"),
                "item": absolute_url(site_url, f"/posts/{p.get('slug')}")
                if p.get("slug")
                else None,
            }
            for idx, p in enumerate(posts)
        ],
    }

    jsonld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": f"{canonical}#collection",
        "url": canonical,
        "name": topic_label,
        "description": topic_description or None,
        "about": {"@id": f"{home}#oliver-ernster"},
        "isPartOf": {"@id": f"{home}#website"},
        "mainEntity": item_list,
    }

    breadcrumb_jsonld = {
        "@context": "https://schema.org",
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
                "name": "Topics",
                "item": absolute_url(site_url, "/topics"),
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": topic_label,
                "item": canonical,
            },
        ],
    }

    ctx.update(
        {
            "is_homepage": False,
            "page_title": f"{topic_label} | Topics | Crank The Code",
            "og_title": f"{topic_label} | Topics | Crank The Code",
            "og_description": topic_description
            or f"Posts in {topic_label} (Decision Architecture).",
            "meta_description": topic_description
            or f"Posts in {topic_label} (Decision Architecture).",
            "topic": {
                "layer": topic_slug,
                "label": topic_label,
                "description": topic_description,
                "posts_index_href": _posts_href(
                    query=None,
                    cat="Leadership",
                    layer=topic_slug if topic_slug != "general" else None,
                    exclude_blog=None,
                ),
            },
            "posts": posts,
            "topic_hubs": hubs,
            "jsonld_json": json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")),
            "jsonld_extra_json": json.dumps(
                breadcrumb_jsonld, ensure_ascii=False, separators=(",", ":")
            ),
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Topics", "href": "/topics"},
                {"label": topic_label, "href": canonical_path},
            ],
        }
    )

    return templates.TemplateResponse(request, "topic_hub.html", ctx)


@router.get("/help", response_class=HTMLResponse)
async def help_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )
    ctx.update(
        {
            "is_homepage": False,
            "robots_meta": "noindex",
            "page_title": "Help | Crank The Code",
            "og_title": "Help | Crank The Code",
            "og_description": "A deliberately unhelpful help page.",
            "meta_description": "Help page for Crank The Code.",
            "back_link_href": "/",
            "back_link_label": "← Back to home",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Help", "href": "/help"},
            ],
        }
    )
    return templates.TemplateResponse(request, "help.html", ctx)


@router.get("/battlestation", response_class=HTMLResponse)
async def battlestation_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )
    ctx.update(
        {
            "is_homepage": False,
            "page_title": "🖥️ The Battlestation That Ships | Crank The Code",
            "og_title": "🖥️ The Battlestation That Ships | Crank The Code",
            "og_description": (
                "The Command Battlestation - dev cockpit + 3D printer room."
            ),
            "meta_description": (
                "A look at my Command Battlestation: daily driver workstation + "
                "3D printer room."
            ),
            "back_link_href": "/",
            "back_link_label": "← Back to home",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "My battlestation", "href": "/battlestation"},
            ],
            "og_image_url": absolute_url(
                get_site_url(request), "/static/images/command-battlestation1.jpg"
            ),
        }
    )
    return templates.TemplateResponse(request, "battlestation.html", ctx)


@router.get("/posts/{slug}", response_class=HTMLResponse)
async def read_post(
    request: Request,
    slug: str,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    slug_raw = (slug or "").strip()
    # Keep `slug_raw` casing/formatting as provided; repository handles lookup.

    detail = blog.get_post(slug_raw)

    if detail is None:
        return HTMLResponse(content="<h1>404 - Post Not Found</h1>", status_code=404)

    # Keep template compatibility: templates expect `post.content`.
    emoji, title_text = _display_title_parts(
        title=detail.title,
        emoji=getattr(detail, "emoji", None),
    )
    post = {
        "slug": detail.slug,
        "title": detail.title,
        "title_text": title_text,
        "emoji": emoji,
        "date": detail.date,
        "tags": list(detail.tags),
        "blurb": getattr(detail, "blurb", None),
        "one_liner": getattr(detail, "one_liner", None),
        "cover_image_url": detail.cover_image_url,
        "extra_image_urls": list(getattr(detail, "extra_image_urls", [])),
        "content": detail.content_html,
    }
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    # Post-specific SEO.
    site_url = ctx.get("site_url") or DEFAULT_SITE_URL
    canonical = canonical_url_for_request(request, site_url=site_url)
    # SEO meta description: keep it stable and concise; tests expect blurb first.
    description = build_meta_description(
        getattr(detail, "blurb", None),
        fallback=getattr(detail, "one_liner", None),
        default=f"Read {detail.title} on Crank The Code.",
    )

    # Social previews: one-liner reads better when shared.
    og_description = build_meta_description(
        getattr(detail, "one_liner", None),
        fallback=getattr(detail, "blurb", None),
        default=description,
    )

    subtitle = (
        getattr(detail, "one_liner", None) or getattr(detail, "blurb", None) or ""
    ).strip()
    og_title = f"{detail.title} - {subtitle}" if subtitle else detail.title

    og_image = (
        getattr(detail, "social_image_url", None)
        or detail.cover_image_url
        or absolute_url(site_url, "/static/images/me.jpg")
    )
    og_image = absolute_url(site_url, og_image)

    # Bonus SEO sauce: for project posts, add SoftwareApplication schema.
    is_project = bool(
        getattr(detail, "one_liner", None) or getattr(detail, "blurb", None)
    )
    if is_project:
        app_jsonld = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": detail.title,
            "operatingSystem": "Cross-platform",
            "applicationCategory": "Developer Tool",
            "description": og_description,
            "author": {"@type": "Person", "name": "Oliver Ernster"},
            "url": canonical,
        }
        ctx["jsonld_extra_json"] = json.dumps(
            app_jsonld, ensure_ascii=False, separators=(",", ":")
        )

    published_iso = to_iso_date(detail.date)
    published_dt = to_iso_datetime(detail.date)

    jsonld: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": detail.title,
        "author": {"@type": "Person", "name": "Oliver Ernster"},
        "mainEntityOfPage": canonical,
        "url": canonical,
        "description": description,
    }
    if published_iso:
        jsonld["datePublished"] = published_iso
        # We don't currently track modified time; use published as a stable fallback.
        jsonld["dateModified"] = published_iso
    if detail.cover_image_url:
        jsonld["image"] = [absolute_url(site_url, detail.cover_image_url)]

    tags = [str(t).strip() for t in (detail.tags or []) if str(t).strip()]
    if tags:
        jsonld["keywords"] = ", ".join(tags)

    breadcrumb_jsonld = {
        "@context": "https://schema.org",
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
                "name": "Posts",
                "item": absolute_url(site_url, "/posts"),
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": detail.title,
                "item": canonical,
            },
        ],
    }

    ctx.update(
        {
            "post": post,
            "is_homepage": False,
            "page_title": f"{og_title} | Crank The Code",
            "canonical_url": canonical,
            "meta_description": description,
            "og_title": og_title,
            "og_description": og_description,
            "og_type": "article",
            "og_image_url": og_image,
            "og_image_alt": detail.title,
            "jsonld_json": json.dumps(
                jsonld, ensure_ascii=False, separators=(",", ":")
            ),
            "jsonld_extra_json": json.dumps(
                breadcrumb_jsonld, ensure_ascii=False, separators=(",", ":")
            ),
            "article_published_time": published_dt,
            "article_modified_time": published_dt,
            "back_link_href": "/posts",
            "back_link_label": "← Back to posts",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Posts", "href": "/posts"},
                {"label": detail.title, "href": f"/posts/{detail.slug}"},
            ],
        }
    )

    # Orientation layer: enrich Start Here with structural navigation without
    # rewriting the underlying markdown.
    if (detail.slug or "").strip().lower() == "start-here":
        hubs = _leadership_topic_hubs(blog)
        recommendations: list[dict[str, object]] = []
        for h in hubs:
            layer = str(h.get("layer") or "").strip()
            layer_posts = _topic_posts_for_layer(blog, layer_slug=layer)[:3]
            recommendations.append(
                {
                    "layer": layer,
                    "label": h.get("label"),
                    "href": h.get("href"),
                    "posts": layer_posts,
                }
            )
        ctx["start_here"] = {
            "author_href": "/about",
            "topics_href": "/topics",
            "topic_hubs": hubs,
            "recommended_by_topic": recommendations,
        }

    resp = templates.TemplateResponse(request, "post.html", ctx)
    # Dev-only safety: clear browser HTTP cache to avoid sticky cached redirects
    # while iterating on legacy slug behavior.
    hostname = (request.url.hostname or "").strip().lower()
    if hostname in {"127.0.0.1", "localhost"}:
        resp.headers["Clear-Site-Data"] = '"cache"'
    return resp
