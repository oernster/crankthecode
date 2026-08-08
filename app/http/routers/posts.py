"""Post listing and post detail routes."""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.domain.tags import humanize_layer_slug, normalize_layer_slug
from app.http.deps import get_blog_service, get_templates
from app.http.seo import (
    DEFAULT_SITE_URL,
    absolute_url,
    canonical_url_for_request,
    to_iso_datetime,
)
from app.http.view_models.context import build_base_context
from app.http.view_models.post_detail import (
    build_article_jsonld,
    build_breadcrumb_jsonld,
    build_descriptions,
    build_navigation,
    build_og_image,
    build_og_title,
    build_post_row,
    first_cat_tag,
    is_essay_post,
)
from app.http.view_models.posts import (
    PILL_GROUP_SIZE,
    category_label_for_query,
    estimate_read_time_minutes,
    group_posts_by_cat,
)
from app.http.view_models.posts_index import (
    build_index_breadcrumbs,
    build_index_rows,
    build_index_titles,
    filter_rows_by_cat,
    filter_rows_by_layer,
    resolve_cat_label,
)
from app.http.view_models.sidebar import (
    POSTS_VIEW_ARCHIVE,
    POSTS_VIEW_WRITING,
    build_sidebar_categories,
    normalize_posts_view,
    posts_view_from_legacy_exclude_blog,
    posts_view_href,
    sidebar_label_with_emoji,
)
from app.services.blog_service import BlogService

router = APIRouter()

# Retired project write-ups. The essays duplicated the per-project landing
# pages on the portfolio hub, so the posts were removed and each old slug now
# redirects permanently to its canonical home. Keys compare case-insensitively.
_PORTFOLIO_HUB_URL = "https://ernster.dev"

_LEGACY_POST_REDIRECTS: dict[str, str] = {
    "3d-printer-launcher": f"{_PORTFOLIO_HUB_URL}/3D-Printer-Launcher/",
    "3d-printing-info": f"{_PORTFOLIO_HUB_URL}/3D-printing-info/",
    "audiodeck": f"{_PORTFOLIO_HUB_URL}/AudioDeck/",
    "axisdb": f"{_PORTFOLIO_HUB_URL}/tooling.html",
    "clearbudget": f"{_PORTFOLIO_HUB_URL}/ClearBudget/",
    "commandfixer": f"{_PORTFOLIO_HUB_URL}/CommandFixer/",
    "edcolonisationasst": f"{_PORTFOLIO_HUB_URL}/EDColonisationAsst/",
    "elevator": f"{_PORTFOLIO_HUB_URL}/elevator/",
    "fancy-clock": f"{_PORTFOLIO_HUB_URL}/FancyClock/",
    "fulcrum": f"{_PORTFOLIO_HUB_URL}/fulcrum/",
    "galacticunicorn": _PORTFOLIO_HUB_URL,
    "latencylab": f"{_PORTFOLIO_HUB_URL}/latencylab/",
    "locus": f"{_PORTFOLIO_HUB_URL}/locus/",
    "meridian": f"{_PORTFOLIO_HUB_URL}/meridian/",
    "mmsp": f"{_PORTFOLIO_HUB_URL}/MMSP-Spec/",
    "narratex": "https://narratex.co.uk",
    "numismatism": f"{_PORTFOLIO_HUB_URL}/coin-analysis/",
    "o7debrief": f"{_PORTFOLIO_HUB_URL}/o7Debrief/",
    "pigeonpost": "https://pigeonpost.ink",
    "postal-gambit": f"{_PORTFOLIO_HUB_URL}/postal-gambit/",
    "snarkapi": "https://www.snarkapi.com",
}

# Legacy post aliases: serve the *new* post content at an old public slug.
# Keys are compared case-insensitively.
_LEGACY_POST_ALIASES: dict[str, str] = {
    "oodathesisdistilled": "what-is-decision-architecture",
    "oodaintro": "what-is-decision-architecture",
}

_LOCAL_HOSTS = {"127.0.0.1", "localhost"}


def _dump_jsonld(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def _rendered(
    request: Request,
    templates: Jinja2Templates,
    template_name: str,
    ctx: dict[str, Any],
):
    """Render a template, clearing the local cache when served from loopback."""

    resp = templates.TemplateResponse(request, template_name, ctx)
    if (request.url.hostname or "").strip().lower() in _LOCAL_HOSTS:
        resp.headers["Clear-Site-Data"] = '"cache"'
    return resp


@router.get("/posts", response_class=HTMLResponse)
async def posts_index(
    request: Request,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    rows = build_index_rows(blog)

    ctx = build_base_context(request)
    current_q = (ctx.get("current_q", "") or "").strip()

    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    cat_label = resolve_cat_label(
        current_cat=(ctx.get("current_cat", "") or "").strip(),
        current_q=current_q,
    )
    current_layer_raw = (ctx.get("current_layer", "") or "").strip()
    layer_slug = normalize_layer_slug(current_layer_raw) if current_layer_raw else None

    ctx["current_cat"] = cat_label or ""
    ctx["current_layer"] = layer_slug or ""

    view_norm = normalize_posts_view(request.query_params.get("view"))
    legacy_view = (
        None
        if view_norm
        else posts_view_from_legacy_exclude_blog(
            request.query_params.get("exclude_blog")
        )
    )
    current_view = view_norm or legacy_view or POSTS_VIEW_WRITING
    ctx["current_view"] = current_view

    # Category and layer narrow the list together, as an AND.
    if cat_label:
        rows = filter_rows_by_cat(rows, cat_label)
    if layer_slug:
        rows = filter_rows_by_layer(rows, layer_slug)

    category_label = (
        sidebar_label_with_emoji(cat_label)
        if cat_label
        else category_label_for_query(current_q, blog=blog, exclude_blog=False)
    )
    layer_label = humanize_layer_slug(layer_slug) if layer_slug else None

    ctx.update(
        {
            "posts": rows,
            "posts_grouped": group_posts_by_cat(
                rows,
                view=current_view,
                exclude_hub_cats=not cat_label,
            ),
            "pill_group_size": PILL_GROUP_SIZE,
            "is_homepage": False,
            "writing_href": posts_view_href(
                view=POSTS_VIEW_WRITING,
                query=current_q or None,
                cat=cat_label,
                layer=layer_slug,
            ),
            "archive_href": posts_view_href(
                view=POSTS_VIEW_ARCHIVE,
                query=current_q or None,
                cat=cat_label,
                layer=layer_slug,
            ),
            "breadcrumb_items": build_index_breadcrumbs(
                view=current_view,
                cat_label=cat_label,
                category_label=category_label,
                layer_label=layer_label,
                filtered_href=posts_view_href(
                    view=current_view,
                    query=None,
                    cat=cat_label,
                    layer=layer_slug,
                ),
            ),
            **build_index_titles(
                cat_label=cat_label,
                category_label=category_label,
                layer_label=layer_label,
            ),
        }
    )

    return _rendered(request, templates, "posts.html", ctx)


@router.get("/posts/{slug}", response_class=HTMLResponse)
async def read_post(
    request: Request,
    slug: str,
    blog: BlogService = Depends(get_blog_service),
    templates: Jinja2Templates = Depends(get_templates),
):
    slug_raw = (slug or "").strip()

    redirect_target = _LEGACY_POST_REDIRECTS.get(slug_raw.strip().lower())
    if redirect_target:
        return RedirectResponse(
            url=redirect_target,
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )

    alias_target = _LEGACY_POST_ALIASES.get(slug_raw.strip().lower())
    canonical_slug = alias_target or slug_raw
    detail = blog.get_post(alias_target or slug_raw)

    if detail is None:
        return HTMLResponse(content="<h1>404 - Post Not Found</h1>", status_code=404)

    cat_tag = first_cat_tag(list(detail.tags))
    is_essay = is_essay_post(detail, cat_tag)

    ctx = build_base_context(request)
    ctx["sidebar_categories"] = build_sidebar_categories(
        blog, exclude_blog=bool(ctx.get("exclude_blog"))
    )

    site_url = ctx.get("site_url") or DEFAULT_SITE_URL

    if alias_target:
        # An alias serves the canonical post's content at an old slug, so point
        # the canonical link at the real one and keep the alias out of the index.
        canonical = absolute_url(site_url, f"/posts/{canonical_slug}")
        ctx["robots_meta"] = "noindex,follow"
    else:
        canonical = canonical_url_for_request(request, site_url=site_url)

    description, og_description = build_descriptions(detail)
    og_title = build_og_title(detail)
    published_dt = to_iso_datetime(detail.date)

    ctx.update(
        {
            "post": build_post_row(detail),
            "is_homepage": False,
            "show_read_time": True,
            "read_time_minutes": estimate_read_time_minutes(detail.content_html or ""),
            "page_title": f"{og_title} | Crank The Code",
            "canonical_url": canonical,
            "meta_description": description,
            "og_title": og_title,
            "og_description": og_description,
            "og_type": "article",
            "og_image_url": build_og_image(detail, site_url=site_url),
            "og_image_alt": detail.title,
            "og_image_width": None,
            "og_image_height": None,
            "jsonld_json": _dump_jsonld(
                build_article_jsonld(
                    detail,
                    canonical=canonical,
                    description=description,
                    site_url=site_url,
                )
            ),
            "jsonld_extra_json": _dump_jsonld(
                build_breadcrumb_jsonld(
                    detail,
                    canonical=canonical,
                    site_url=site_url,
                    is_essay=is_essay,
                )
            ),
            "article_published_time": published_dt,
            "article_modified_time": published_dt,
            **build_navigation(detail, cat_tag=cat_tag, is_essay=is_essay),
        }
    )

    return _rendered(request, templates, "post.html", ctx)
