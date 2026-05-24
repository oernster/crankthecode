from __future__ import annotations

"""Topics, patterns, and decision architecture routes."""

import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.domain.tags import humanize_layer_slug
from app.domain.taxonomy import (
    PATTERNS_CAT_TAG,
    PATTERNS_LAYER_EMOJIS,
    PATTERNS_LAYER_LABELS,
    PATTERNS_LAYER_ORDER,
    STRUCTURES_LAYER_EMOJIS,
    STRUCTURES_LAYER_ORDER,
)
from app.http.deps import get_blog_service, get_templates
from app.http.seo import absolute_url, get_site_url
from app.http.view_models.context import build_base_context
from app.http.view_models.leadership import (
    build_leadership_topic_hubs,
    category_posts_grouped_by_layer,
    homepage_leadership_items,
    patterns_posts_for_layer,
    topic_layer_slug_for_route,
    topic_posts_for_layer,
)
from app.http.view_models.posts import post_frontmatter_emoji_index
from app.http.view_models.sidebar import build_sidebar_categories, posts_href
from app.services.blog_service import BlogService

router = APIRouter()


@router.get("/decision-architecture", response_class=HTMLResponse)
async def decision_architecture_gateway(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    """Gateway page for Decision Architecture content."""

    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    emoji_index = post_frontmatter_emoji_index(blog)

    layers = sorted(
        [
            {
                "layer": slug,
                "label": humanize_layer_slug(slug),
                "emoji": STRUCTURES_LAYER_EMOJIS.get(slug, ""),
                "href": f"/topics/{slug}",
            }
            for slug in STRUCTURES_LAYER_ORDER
        ],
        key=lambda d: d["label"].lower(),
    )

    ctx.update(
        {
            "is_homepage": False,
            "page_title": "Decision Architecture | Crank The Code",
            "og_title": "Decision Architecture | Crank The Code",
            "og_description": "Decision Architecture posts grouped by layer.",
            "meta_description": "Decision Architecture posts grouped by layer.",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Decision Architecture", "href": "/decision-architecture"},
            ],
            "groups": homepage_leadership_items(blog),
            "layers": layers,
            "emoji_index": emoji_index,
        }
    )

    return templates.TemplateResponse(request, "decision_architecture.html", ctx)


@router.get("/patterns", response_class=HTMLResponse)
async def patterns_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    """Gateway page for Decision Architecture Patterns."""

    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    emoji_index = post_frontmatter_emoji_index(blog)
    groups = category_posts_grouped_by_layer(
        blog,
        cat_tag=PATTERNS_CAT_TAG,
        layer_label_overrides=PATTERNS_LAYER_LABELS,
    )

    layers = sorted(
        [
            {
                "layer": slug,
                "label": PATTERNS_LAYER_LABELS[slug],
                "emoji": PATTERNS_LAYER_EMOJIS.get(slug, ""),
                "href": f"/patterns/{slug}",
            }
            for slug in PATTERNS_LAYER_ORDER
        ],
        key=lambda d: d["label"].lower(),
    )

    ctx.update(
        {
            "is_homepage": False,
            "page_title": "Decision Architecture Patterns | Crank The Code",
            "og_title": "Decision Architecture Patterns | Crank The Code",
            "og_description": "Reusable organisational design patterns derived from Decision Architecture thinking.",
            "meta_description": "Reusable organisational design patterns derived from Decision Architecture thinking.",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Decision Architecture Patterns", "href": "/patterns"},
            ],
            "description": "Reusable organisational design patterns derived from Decision Architecture thinking.",
            "layers": layers,
            "groups": groups,
            "emoji_index": emoji_index,
        }
    )

    return templates.TemplateResponse(request, "patterns_index.html", ctx)


@router.get("/patterns/{layer_slug}", response_class=HTMLResponse)
async def patterns_layer_page(
    request: Request,
    layer_slug: str,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    cleaned = topic_layer_slug_for_route(layer_slug)
    if cleaned == "general":
        label = "General"
    else:
        label = PATTERNS_LAYER_LABELS.get(cleaned, humanize_layer_slug(cleaned))

    posts = patterns_posts_for_layer(blog, layer_slug=cleaned)

    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    site_url = get_site_url(request)
    canonical_path = f"/patterns/{cleaned}"
    canonical = absolute_url(site_url, canonical_path)

    ctx.update(
        {
            "is_homepage": False,
            "canonical_url": canonical,
            "page_title": f"{label} | Patterns | Crank The Code",
            "og_title": f"{label} | Patterns | Crank The Code",
            "og_description": f"Posts in {label} (Decision Architecture Patterns).",
            "meta_description": f"Posts in {label} (Decision Architecture Patterns).",
            "breadcrumb_items": [
                {"label": "Home", "href": "/"},
                {"label": "Decision Architecture Patterns", "href": "/patterns"},
                {"label": label, "href": canonical_path},
            ],
            "hub": {"layer": cleaned, "label": label, "description": ""},
            "layers": sorted(
                [
                    {
                        "layer": slug,
                        "label": PATTERNS_LAYER_LABELS[slug],
                        "emoji": PATTERNS_LAYER_EMOJIS.get(slug, ""),
                        "href": f"/patterns/{slug}",
                    }
                    for slug in PATTERNS_LAYER_ORDER
                ],
                key=lambda d: d["label"].lower(),
            ),
            "current_layer": cleaned,
            "posts": posts,
        }
    )

    return templates.TemplateResponse(request, "patterns_hub.html", ctx)


@router.get("/topics", response_class=HTMLResponse)
async def topics_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    hubs = build_leadership_topic_hubs(blog)

    structures_layers = sorted(
        [
            {
                "layer": slug,
                "label": humanize_layer_slug(slug),
                "emoji": STRUCTURES_LAYER_EMOJIS.get(slug, ""),
                "href": f"/topics/{slug}",
            }
            for slug in STRUCTURES_LAYER_ORDER
        ],
        key=lambda d: d["label"].lower(),
    )

    patterns_layers = sorted(
        [
            {
                "layer": slug,
                "label": PATTERNS_LAYER_LABELS.get(slug, humanize_layer_slug(slug)),
                "emoji": PATTERNS_LAYER_EMOJIS.get(slug, ""),
                "href": f"/patterns/{slug}",
            }
            for slug in PATTERNS_LAYER_ORDER
        ],
        key=lambda d: d["label"].lower(),
    )

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

    collection_page = {
        "@type": "CollectionPage",
        "@id": f"{canonical}#collection",
        "url": canonical,
        "name": "Topics",
        "about": {"@id": f"{home}#oliver-ernster"},
        "isPartOf": {"@id": f"{home}#website"},
        "mainEntity": item_list,
    }

    # DefinedTermSet signals the full topic taxonomy as a machine-readable
    # vocabulary. Stronger than a plain CollectionPage for topical authority.
    defined_term_set = {
        "@type": "DefinedTermSet",
        "@id": f"{canonical}#taxonomy",
        "name": "Decision Architecture Topics",
        "url": canonical,
        "hasDefinedTerm": [
            {
                "@type": "DefinedTerm",
                "name": layer["label"],
                "url": absolute_url(site_url, str(layer["href"])),
            }
            for layer in structures_layers
        ]
        + [
            {
                "@type": "DefinedTerm",
                "name": layer["label"],
                "url": absolute_url(site_url, str(layer["href"])),
            }
            for layer in patterns_layers
        ],
    }

    jsonld = {
        "@context": "https://schema.org",
        "@graph": [collection_page, defined_term_set],
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
            "structures_layers": structures_layers,
            "patterns_layers": patterns_layers,
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
    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    topic_slug = topic_layer_slug_for_route(layer_slug)
    hubs = build_leadership_topic_hubs(blog)

    hub = next((h for h in hubs if (h.get("layer") or "") == topic_slug), None)
    topic_label = (
        str(hub.get("label"))
        if hub is not None
        else (humanize_layer_slug(topic_slug) if topic_slug != "general" else "General")
    )
    topic_description = str(hub.get("description") or "") if hub is not None else ""

    posts = topic_posts_for_layer(blog, layer_slug=topic_slug)

    layers = sorted(
        [
            {
                "layer": slug,
                "label": humanize_layer_slug(slug),
                "emoji": STRUCTURES_LAYER_EMOJIS.get(slug, ""),
                "href": f"/topics/{slug}",
            }
            for slug in STRUCTURES_LAYER_ORDER
        ],
        key=lambda d: d["label"].lower(),
    )

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
                "posts_index_href": posts_href(
                    query=None,
                    cat="Leadership",
                    layer=topic_slug if topic_slug != "general" else None,
                    exclude_blog=None,
                ),
            },
            "posts": posts,
            "layers": layers,
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
