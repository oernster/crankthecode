from __future__ import annotations

"""Post listing and post detail routes."""

import json
from collections.abc import Mapping
from typing import cast

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.http.deps import get_blog_service, get_templates
from app.http.seo import (
    DEFAULT_SITE_URL,
    absolute_url,
    build_meta_description,
    canonical_url_for_request,
    get_site_url,
    to_iso_date,
    to_iso_datetime,
)
from app.http.view_models.context import build_base_context
from app.http.view_models.posts import (
    PILL_GROUP_SIZE,
    category_label_for_query,
    display_title_parts,
    estimate_read_time_minutes,
    group_posts_by_cat,
    is_project_post_by_tags,
    post_emoji_map,
    post_frontmatter_emoji_index,
    split_leading_emoji_from_title,
)
from app.http.view_models.sidebar import (
    POSTS_VIEW_ARCHIVE,
    POSTS_VIEW_PROJECTS,
    POSTS_VIEW_WRITING,
    build_sidebar_categories,
    normalize_cat_label,
    normalize_layer_slug,
    normalize_posts_view,
    posts_base_href,
    posts_href,
    posts_view_from_legacy_exclude_blog,
    posts_view_href,
)
from app.domain.taxonomy import PROJECT_CATEGORY_LABELS
from app.domain.tags import humanize_layer_slug, primary_layer_slug_from_tags
from app.services.blog_service import BlogService

router = APIRouter()

_LEGACY_POST_REDIRECTS: dict[str, str] = {}

# Legacy post aliases: serve the *new* post content at an old public slug.
# Keys are compared case-insensitively.
_LEGACY_POST_ALIASES: dict[str, str] = {
    "oodathesisdistilled": "what-is-decision-architecture",
    "oodaintro": "what-is-decision-architecture",
}

_CAT_TAG_PREFIX = "cat:"


@router.get("/posts", response_class=HTMLResponse)
async def posts_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    emoji_map = post_emoji_map()
    posts = [
        (
            lambda _p: (
                {
                    "slug": _p.slug,
                    "title": _p.title,
                    "title_text": display_title_parts(
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
                    "emoji": display_title_parts(
                        title=_p.title,
                        emoji=(
                            getattr(_p, "emoji", None) or emoji_map.get(_p.slug, "")
                        ),
                    )[0],
                    "summary_html": _p.summary_html,
                }
            )
        )(p)
        for p in blog.list_posts()
    ]

    hidden_slugs = {"about-me", "about", "start-here", "portfolio"}
    posts = [
        p for p in posts if str(p.get("slug", "")).strip().lower() not in hidden_slugs
    ]
    ctx = build_base_context(request)
    current_q = (ctx.get("current_q", "") or "").strip()
    current_cat_raw = (ctx.get("current_cat", "") or "").strip()
    current_layer_raw = (ctx.get("current_layer", "") or "").strip()

    ctx["sidebar_categories"] = build_sidebar_categories(blog, exclude_blog=bool(ctx.get("exclude_blog")))

    cat_label: str | None = None
    if current_cat_raw:
        cat_label = normalize_cat_label(current_cat_raw)
    elif (
        current_q.lower().startswith(_CAT_TAG_PREFIX)
        and current_q.strip().lower() != _CAT_TAG_PREFIX
    ):
        tail = current_q.split(":", 1)[1].strip()
        cat_label = normalize_cat_label(tail) if tail else None

    layer_slug: str | None = None
    if current_layer_raw:
        layer_slug = normalize_layer_slug(current_layer_raw)

    ctx["current_cat"] = cat_label or ""
    ctx["current_layer"] = layer_slug or ""

    view_norm = normalize_posts_view(request.query_params.get("view"))
    legacy_view = (
        None
        if view_norm
        else posts_view_from_legacy_exclude_blog(request.query_params.get("exclude_blog"))
    )

    cat_norm = (cat_label or "").strip().lower()
    default_view = (
        POSTS_VIEW_PROJECTS if cat_norm in PROJECT_CATEGORY_LABELS else POSTS_VIEW_WRITING
    )
    current_view = view_norm or legacy_view or default_view
    ctx["current_view"] = current_view

    # Content-type filtering (primary)
    if current_view == POSTS_VIEW_WRITING:
        posts = [
            p for p in posts
            if not is_project_post_by_tags(
                str(p.get("post_type") or ""),
                [str(t) for t in cast(list[object], p.get("tags") or [])],
            )
        ]
    elif current_view == POSTS_VIEW_PROJECTS:
        posts = [
            p for p in posts
            if is_project_post_by_tags(
                str(p.get("post_type") or ""),
                [str(t) for t in cast(list[object], p.get("tags") or [])],
            )
        ]
    elif current_view == POSTS_VIEW_ARCHIVE:
        posts = posts
    else:  # pragma: no cover
        posts = [
            p for p in posts
            if not is_project_post_by_tags(
                str(p.get("post_type") or ""),
                [str(t) for t in cast(list[object], p.get("tags") or [])],
            )
        ]

    # Server-side filtering for category + layer (AND semantics).
    if cat_label:
        from app.http.view_models.sidebar import extract_category_queries_from_tags
        cat_tag_norm = f"cat:{normalize_cat_label(cat_label)}".strip().lower()
        posts = [
            p
            for p in posts
            if any(
                (q or "").strip().lower() == cat_tag_norm
                for q in extract_category_queries_from_tags(
                    [str(t) for t in (p.get("tags") or [])]
                )
            )
        ]

    if layer_slug:
        from app.domain.tags import extract_layer_slugs_from_tags
        layer_tag_norm = f"layer:{normalize_layer_slug(layer_slug)}".strip().lower()
        posts = [
            p
            for p in posts
            if any(
                f"layer:{s}".strip().lower() == layer_tag_norm
                for s in extract_layer_slugs_from_tags(
                    [str(t) for t in (p.get("tags") or [])]
                )
            )
        ]

    category_label = None
    if cat_label:
        from app.http.view_models.sidebar import sidebar_label_with_emoji
        category_label = sidebar_label_with_emoji(cat_label)
    else:
        category_label = category_label_for_query(current_q, blog=blog, exclude_blog=False)

    layer_label = humanize_layer_slug(layer_slug) if layer_slug else None

    page_title = "Posts | Crank The Code"
    og_title = "Posts | Crank The Code"
    og_description = "Browse all Crank The Code posts and project write-ups."
    meta_description = "Browse all Crank The Code posts and project write-ups."
    if cat_label:
        cat_display = (category_label or cat_label).strip()
        _, cat_text = split_leading_emoji_from_title(cat_display)
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
            meta_description = meta_description  # pragma: no cover

    writing_href = posts_view_href(
        view=POSTS_VIEW_WRITING, query=current_q or None, cat=cat_label, layer=layer_slug,
    )
    projects_href = posts_view_href(
        view=POSTS_VIEW_PROJECTS, query=current_q or None, cat=cat_label, layer=layer_slug,
    )
    archive_href = posts_view_href(
        view=POSTS_VIEW_ARCHIVE, query=current_q or None, cat=cat_label, layer=layer_slug,
    )
    filtered_href = posts_view_href(
        view=current_view, query=None, cat=cat_label, layer=layer_slug,
    )

    ctx.update(
        {
            "posts": posts,
            "posts_grouped": group_posts_by_cat(posts, view=current_view),
            "pill_group_size": PILL_GROUP_SIZE,
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
                {"label": "Posts", "href": posts_base_href(view=current_view)},
                *(
                    [
                        {
                            "label": category_label or cat_label,
                            "href": posts_href(
                                query=None, cat=cat_label, layer=None, exclude_blog=None,
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
    hostname = (request.url.hostname or "").strip().lower()
    if hostname in {"127.0.0.1", "localhost"}:
        resp.headers["Clear-Site-Data"] = '"cache"'
    return resp


@router.get("/posts/{slug}", response_class=HTMLResponse)
async def read_post(
    request: Request,
    slug: str,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    slug_raw = (slug or "").strip()

    alias_target = _LEGACY_POST_ALIASES.get(slug_raw.strip().lower())
    canonical_slug = alias_target or slug_raw
    lookup_slug = alias_target or slug_raw

    detail = blog.get_post(lookup_slug)

    if detail is None:
        return HTMLResponse(content="<h1>404 - Post Not Found</h1>", status_code=404)

    emoji, title_text = display_title_parts(
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

    def _first_cat_tag(tags: list[str]) -> str:
        for t in tags or []:
            t_norm = str(t or "").strip()
            if t_norm.lower().startswith("cat:"):
                return t_norm
        return ""

    cat_tag = _first_cat_tag(post.get("tags") or [])
    cat_norm = cat_tag.lower()
    if cat_norm == "cat:leadership":
        back_link_href = "/decision-architecture"
        back_link_label = "← Back to Decision Architecture"
        breadcrumb_items = [
            {"label": "Home", "href": "/"},
            {"label": "Decision Architecture", "href": "/decision-architecture"},
            {"label": detail.title, "href": f"/posts/{detail.slug}"},
        ]
    elif cat_norm == "cat:decision-architecture-patterns":
        back_link_href = "/patterns"
        back_link_label = "← Back to Patterns"
        breadcrumb_items = [
            {"label": "Home", "href": "/"},
            {"label": "Decision Architecture Patterns", "href": "/patterns"},
            {"label": detail.title, "href": f"/posts/{detail.slug}"},
        ]
    else:
        back_link_href = "/posts"
        back_link_label = "← Back to posts"
        breadcrumb_items = [
            {"label": "Home", "href": "/"},
            {"label": "Posts", "href": "/posts"},
            {"label": detail.title, "href": f"/posts/{detail.slug}"},
        ]

    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    site_url = ctx.get("site_url") or DEFAULT_SITE_URL

    if alias_target:
        canonical = absolute_url(site_url, f"/posts/{canonical_slug}")
        ctx["robots_meta"] = "noindex,follow"
    else:
        canonical = canonical_url_for_request(request, site_url=site_url)

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
        jsonld["dateModified"] = published_iso
    if detail.cover_image_url:
        jsonld["image"] = [absolute_url(site_url, detail.cover_image_url)]

    tags = [str(t).strip() for t in (detail.tags or []) if str(t).strip()]
    if tags:
        jsonld["keywords"] = ", ".join(tags)

    # For leadership posts with a layer tag, route the JSON-LD breadcrumb
    # through the topic hub. This creates a hub-and-spoke graph that Google
    # uses to infer topical clusters. Invisible to users, high signal to crawlers.
    post_tags_for_layer = [str(t) for t in (detail.tags or [])]
    from app.http.view_models.leadership import is_leadership_post
    _is_leadership = is_leadership_post(post_tags_for_layer)
    _primary_layer = (
        primary_layer_slug_from_tags(post_tags_for_layer) if _is_leadership else None
    )

    if _primary_layer:
        _layer_label = humanize_layer_slug(_primary_layer)
        breadcrumb_items_jsonld = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": absolute_url(site_url, "/")},
            {"@type": "ListItem", "position": 2, "name": "Topics", "item": absolute_url(site_url, "/topics")},
            {"@type": "ListItem", "position": 3, "name": _layer_label, "item": absolute_url(site_url, f"/topics/{_primary_layer}")},
            {"@type": "ListItem", "position": 4, "name": detail.title, "item": canonical},
        ]
    else:
        breadcrumb_items_jsonld = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": absolute_url(site_url, "/")},
            {"@type": "ListItem", "position": 2, "name": "Posts", "item": absolute_url(site_url, "/posts")},
            {"@type": "ListItem", "position": 3, "name": detail.title, "item": canonical},
        ]

    breadcrumb_jsonld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumb_items_jsonld,
    }

    # Reading time: estimate from rendered HTML content.
    read_time = estimate_read_time_minutes(detail.content_html or "")

    ctx.update(
        {
            "post": post,
            "is_homepage": False,
            "show_read_time": True,
            "read_time_minutes": read_time,
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
            "back_link_href": back_link_href,
            "back_link_label": back_link_label,
            "breadcrumb_items": breadcrumb_items,
        }
    )

    resp = templates.TemplateResponse(request, "post.html", ctx)
    hostname = (request.url.hostname or "").strip().lower()
    if hostname in {"127.0.0.1", "localhost"}:
        resp.headers["Clear-Site-Data"] = '"cache"'
    return resp
