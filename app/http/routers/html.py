from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import cast
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
    to_iso_date,
)
from app.services.blog_service import BlogService
from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.adapters.markdown_python_renderer import PythonMarkdownRenderer

router = APIRouter()

_CAT_TAG_PREFIX = "cat:"
_CAT_TAG_BLOG = "cat:blog"


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
        "hardware": "🔧 Hardware",
        "leadership": "♟️ Leadership",
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


def _is_blog_post_by_cat(tags: list[str]) -> bool:
    return any((t or "").strip().lower() == _CAT_TAG_BLOG for t in (tags or []))


def _posts_href(*, query: str | None, exclude_blog: bool | None) -> str:
    parts: list[str] = []
    if query:
        parts.append(f"q={quote(query, safe='')}")
    if exclude_blog is not None:
        parts.append(f"exclude_blog={'1' if exclude_blog else '0'}")
    return "/posts" + ("?" + "&".join(parts) if parts else "")


def _sidebar_categories(blog: BlogService, *, exclude_blog: bool) -> list[dict[str, str]]:
    """Build sidebar categories from explicit `cat:` tags.

    Category links always point to `/posts?q=cat:<Label>`.
    When blog posts are included (`exclude_blog=False`), the category links
    preserve that choice by including `exclude_blog=0` in the URL.
    """

    key_to_query: dict[str, str] = {}
    for p in blog.list_posts():
        tags = [str(t) for t in (p.tags or [])]
        for q in _extract_category_queries_from_tags(tags):
            key = q.lower()
            key_to_query.setdefault(key, q)

    queries = sorted(key_to_query.values(), key=lambda s: s.lower())
    out: list[dict[str, str]] = []
    for q in queries:
        label = q.split(":", 1)[1].strip() if ":" in q else q
        label = _sidebar_label_with_emoji(label)
        href = _posts_href(query=q, exclude_blog=(False if not exclude_blog else None))
        out.append({"label": label, "query": q, "href": href})
    return out


def _homepage_leadership_items(blog: BlogService) -> list[dict[str, str]]:
    """Homepage Leadership content entries.

    This section must auto-surface leadership posts without any hardcoded slug
    list. We derive it directly from the post metadata:

    - include any post with an *exact* `cat:Leadership` tag (case-insensitive)
    - keep the ordering consistent with `blog.list_posts()` (newest-first)
    - label is the post title
    """

    items: list[dict[str, str]] = []
    for p in blog.list_posts():
        tags_norm = [(str(t) or "").strip().lower() for t in (p.tags or [])]
        if "cat:leadership" not in tags_norm:
            continue
        items.append({"slug": p.slug, "label": p.title, "date": str(p.date or "")})

    # Sort newest-first by the stored `YYYY-MM-DD HH:MM` string format.
    items.sort(key=lambda i: i.get("date", ""), reverse=True)
    return [{"slug": i["slug"], "label": i["label"]} for i in items]


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
        "meta_description": "Crank The Code - Python engineering blog and technical write-ups by Oliver Ernster.",
        # Filled by routes (requires BlogService).
        "sidebar_categories": [],
        "current_q": (request.query_params.get("q") or "").strip(),
        "exclude_blog": exclude_blog,
        "breadcrumb_items": [
            {"label": "Home", "href": "/"},
        ],
    }


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
            "desktop|windows|app|pyside|qt|installer|clock|audio|streamdeck|stellody|trainer": "🖥️ Desktop Apps",
            "gaming|game|elite|dangerous|frontier|colonisation": "🎮 Gaming",
            "tool|tools|cli|utility|utilities|launcher|database|db": "🧰 Tools",
            "api|apis|fastapi|django|rest|web": "🌐 Web APIs",
        }
        return legacy.get(raw)

    for c in _sidebar_categories(blog, exclude_blog=exclude_blog):
        if (c.get("query") or "").strip().lower() == raw.lower():
            return c.get("label")
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


@router.get("/", response_class=HTMLResponse)
async def homepage(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(blog, exclude_blog=bool(ctx.get("exclude_blog")))
    cover_index = _post_cover_index(blog)
    thumb_index = _post_thumb_index(blog)
    blurb_index = _post_blurb_index(blog)
    emoji_index = _post_frontmatter_emoji_index(blog)
    ctx.update(
        {
            "is_homepage": True,
            "og_title": "Crank The Code - Python Engineering Blog by Oliver Ernster",
            "og_description": "Python engineering blog by Oliver Ernster: projects, FastAPI tooling and technical write-ups.",
            "breadcrumb_items": [{"label": "Home", "href": "/"}],
            "homepage_projects": {
                "featured": [
                    {"slug": "stellody", "label": "Stellody"},
                    {"slug": "3D-printing-info", "label": "3D Printing Info"},
                    {"slug": "calendifier", "label": "Calendifier"},
                    {"slug": "trainer", "label": "Trainer"},
                    {"slug": "axisdb", "label": "AxisDB"},
                    {"slug": "edcolonisationasst", "label": "EDColonisationAsst"},
                ],
                "leadership": _homepage_leadership_items(blog),
                "backlog": [
                    # Pinned intro posts (keep first).
                    {"slug": "hello-crank", "label": "Hello Crank"},
                    {"slug": "why-crank", "label": "Why Crank?"},

                    {"slug": "3D-printer-launcher", "label": "3D Printer Launcher"},
                    {"slug": "audiodeck", "label": "Audio Deck"},
                    {"slug": "elevator", "label": "Elevator"},
                    {"slug": "fancy-clock", "label": "Fancy Clock", "emoji": "⏰"},
                    {"slug": "galacticunicorn", "label": "Galactic Unicorn"},
                    {"slug": "numismatism", "label": "Numismatism"},
                    {"slug": "snarkapi", "label": "SnarkAPI"},
                ],
                "tooling": [
                    {
                        "slug": "the-led-problem-the-virpil-community-had",
                        "label": "The LED Problem the Virpil Community Had",
                        "emoji": "💡",
                    },
                    {
                        "slug": "tiny-tools",
                        "label": "Tiny Tools I Refuse to Live Without",
                        "emoji": "🧩",
                    },
                    {
                        "slug": "hardware-guides-are-accidental-bios",
                        "label": "Hardware Guides Are Accidental Biographies",
                        "emoji": "🔧",
                    },
                    {"slug": "bots", "label": "Bots Are Interfaces", "emoji": "🛎️"},
                    {"slug": "niche-tools", "label": "Niche Tools", "emoji": "🧰"},
                    {
                        "slug": "simple-hacking",
                        "label": "Simple Hacking",
                        "emoji": "🛠️",
                    },
                    {
                        "slug": "ai-standard",
                        "label": "On Working with Machines",
                        "emoji": "🤖",
                    },
                ],
            },
            "homepage_cover_index": cover_index,
            "homepage_thumb_index": thumb_index,
            "homepage_blurb_index": blurb_index,
            "homepage_emoji_index": emoji_index,
        }
    )

    # Bonus SEO sauce: SoftwareApplication schema (site-level, for rich previews/search).
    homepage_jsonld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Crank The Code",
        "url": absolute_url(get_site_url(request), "/"),
        "author": {"@type": "Person", "name": "Oliver Ernster"},
    }
    ctx["jsonld_extra_json"] = json.dumps(
        homepage_jsonld, ensure_ascii=False, separators=(",", ":")
    )

    return templates.TemplateResponse(request, "index.html", ctx)


@router.get("/posts", response_class=HTMLResponse)
async def posts_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    emoji_map = _post_emoji_map()
    posts = [
        (lambda _p: (
            {
                "slug": _p.slug,
                "title": _p.title,
                "title_text": _display_title_parts(
                    title=_p.title,
                    emoji=(getattr(_p, "emoji", None) or emoji_map.get(_p.slug, "")),
                )[1],
                "date": _p.date,
                "tags": list(_p.tags),
                "blurb": getattr(_p, "blurb", None),
                "one_liner": getattr(_p, "one_liner", None),
                "cover_image_url": _p.cover_image_url,
                "thumb_image_url": getattr(_p, "thumb_image_url", None),
                "emoji": _display_title_parts(
                    title=_p.title,
                    emoji=(getattr(_p, "emoji", None) or emoji_map.get(_p.slug, "")),
                )[0],
                # Keep links in summaries clickable.
                "summary_html": _p.summary_html,
            }
        ))(p)
        for p in blog.list_posts()
    ]

    # “About me” is rendered on a dedicated `/about` page and should not appear
    # in any post listing (including “All posts (exc. Blog)”).
    posts = [
        p
        for p in posts
        if str(p.get("slug", "")).strip().lower() not in {"about-me", "about"}
    ]
    ctx = _base_context(request)
    current_q = (ctx.get("current_q", "") or "").strip()
    exclude_blog = bool(ctx.get("exclude_blog"))

    # Sidebar categories are tag-driven.
    ctx["sidebar_categories"] = _sidebar_categories(blog, exclude_blog=exclude_blog)

    # Default view: projects only (exclude `cat:Blog`) unless explicitly included.
    # Always include blog posts when the user is explicitly browsing the Blog category.
    if exclude_blog and current_q.strip().lower() != _CAT_TAG_BLOG:
        posts = [
            p
            for p in posts
            if not _is_blog_post_by_cat([str(t) for t in (p.get("tags") or [])])
        ]

    # Deep-links for categories should render server-side filtered HTML (tests and
    # no-JS users). Only apply when `q` is an exact `cat:` query.
    if current_q.lower().startswith(_CAT_TAG_PREFIX) and current_q.strip().lower() != _CAT_TAG_PREFIX:
        q_norm = current_q.strip().lower()
        posts = [
            p
            for p in posts
            if any((str(t).strip().lower() == q_norm) for t in (p.get("tags") or []))
        ]

    category_label = _category_label_for_query(
        current_q, blog=blog, exclude_blog=exclude_blog
    )

    # SEO: category deep-links should have distinct titles/descriptions.
    # Only apply when `q` is an exact `cat:` query (not free-text search).
    page_title = "Posts | Crank The Code"
    og_title = "Posts | Crank The Code"
    og_description = "Browse all Crank The Code posts and project write-ups."
    meta_description = "Browse all Crank The Code posts and project write-ups."
    if current_q.lower().startswith(_CAT_TAG_PREFIX) and current_q.strip().lower() != _CAT_TAG_PREFIX:
        cat_display = (category_label or current_q).strip()
        # Category labels may be emoji-prefixed (e.g. "♟️ Leadership").
        _, cat_text = _split_leading_emoji_from_title(cat_display)
        cat_text = (cat_text or cat_display).strip()
        if cat_text:
            page_title = f"{cat_text} | Posts | Crank The Code"
            og_title = page_title
            og_description = f"Browse posts in {cat_text} on Crank The Code."
            meta_description = og_description

    filtered_href = _posts_href(query=current_q or None, exclude_blog=None)

    projects_only_href = _posts_href(query=current_q or None, exclude_blog=True)
    include_blog_href = _posts_href(query=current_q or None, exclude_blog=False)
    ctx.update(
        {
            "posts": posts,
            "is_homepage": False,
            "page_title": page_title,
            "og_title": og_title,
            "og_description": og_description,
            "meta_description": meta_description,
            "projects_only_href": projects_only_href,
            "include_blog_href": include_blog_href,
            "exclude_blog_effective": exclude_blog and current_q.strip().lower() != _CAT_TAG_BLOG,
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Posts", "href": "/posts"},
                *(
                    [
                        {
                            "label": category_label or current_q,
                            "href": filtered_href,
                        }
                    ]
                    if current_q
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
    ctx["sidebar_categories"] = _sidebar_categories(blog, exclude_blog=bool(ctx.get("exclude_blog")))
    ctx.update(
        {
            "about_html": _load_about_html(),
            "is_homepage": False,
            "page_title": "About me | Crank The Code",
            "og_title": "About me | Crank The Code",
            "og_description": "About Oliver Ernster and the Crank The Code blog.",
            "meta_description": "About Oliver Ernster and the Crank The Code blog.",
            "back_link_href": "/",
            "back_link_label": "← Back to posts",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "About", "href": "/about"},
            ],
        }
    )
    return templates.TemplateResponse(request, "about.html", ctx)


@router.get("/help", response_class=HTMLResponse)
async def help_page(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = _base_context(request)
    ctx["sidebar_categories"] = _sidebar_categories(blog, exclude_blog=bool(ctx.get("exclude_blog")))
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
    ctx["sidebar_categories"] = _sidebar_categories(blog, exclude_blog=bool(ctx.get("exclude_blog")))
    ctx.update(
        {
            "is_homepage": False,
            "page_title": "🖥️ The Battlestation That Ships | Crank The Code",
            "og_title": "🖥️ The Battlestation That Ships | Crank The Code",
            "og_description": "The Command Battlestation - dev cockpit + 3D printer room.",
            "meta_description": "A look at my Command Battlestation: daily driver workstation + 3D printer room.",
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
    slug_norm = slug_raw.lower()

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
    ctx["sidebar_categories"] = _sidebar_categories(blog, exclude_blog=bool(ctx.get("exclude_blog")))

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

    subtitle = (getattr(detail, "one_liner", None) or getattr(detail, "blurb", None) or "").strip()
    og_title = f"{detail.title} - {subtitle}" if subtitle else detail.title

    og_image = (
        getattr(detail, "social_image_url", None)
        or detail.cover_image_url
        or absolute_url(site_url, "/static/images/me.jpg")
    )
    og_image = absolute_url(site_url, og_image)

    # Bonus SEO sauce: for project posts, add SoftwareApplication schema.
    is_project = bool(getattr(detail, "one_liner", None) or getattr(detail, "blurb", None))
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
    jsonld: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": detail.title,
        "author": {"@type": "Person", "name": "Oliver Ernster"},
        "mainEntityOfPage": canonical,
    }
    if published_iso:
        jsonld["datePublished"] = published_iso
    if detail.cover_image_url:
        jsonld["image"] = [absolute_url(site_url, detail.cover_image_url)]

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
            "jsonld_json": json.dumps(jsonld, ensure_ascii=False, separators=(",", ":")),
            "back_link_href": "/posts",
            "back_link_label": "← Back to posts",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Posts", "href": "/posts"},
                {"label": detail.title, "href": f"/posts/{detail.slug}"},
            ],
        }
    )

    resp = templates.TemplateResponse(request, "post.html", ctx)
    # Dev-only safety: clear browser HTTP cache to avoid sticky cached redirects
    # while iterating on legacy slug behavior.
    hostname = (request.url.hostname or "").strip().lower()
    if hostname in {"127.0.0.1", "localhost"}:
        resp.headers["Clear-Site-Data"] = '"cache"'
    return resp
