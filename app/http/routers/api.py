from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.http.seo import absolute_url, build_meta_description, get_site_url

from app.http.schemas import PostDetailResponse, PostSummaryResponse
from app.services.blog_service import BlogService
from app.http.deps import get_blog_service

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/posts", response_model=list[PostSummaryResponse])
async def list_posts(blog: BlogService = Depends(get_blog_service)):
    posts = blog.list_posts()
    return [
        PostSummaryResponse(
            slug=p.slug,
            title=p.title,
            date=p.date,
            tags=list(p.tags),
            summary_html=p.summary_html,
        )
        for p in posts
    ]


@router.get("/posts/{slug}/meta")
async def get_post_meta(slug: str, blog: BlogService = Depends(get_blog_service)):
    """Lightweight meta data for social previews (OpenGraph/Twitter).

    This is intentionally not tied to the public PostDetail schema because it is
    a presentation concern.
    """

    post = blog.get_post(slug)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    site_url = get_site_url(None)
    canonical = absolute_url(site_url, f"/posts/{post.slug}")
    title = post.title
    subtitle = (getattr(post, "one_liner", None) or getattr(post, "blurb", None) or "").strip()
    og_title = f"{title} - {subtitle}" if subtitle else title
    og_description = build_meta_description(
        getattr(post, "one_liner", None),
        fallback=getattr(post, "blurb", None),
        default=f"Read {title} on CrankTheCode.",
    )
    img = post.cover_image_url or "/static/images/me.jpg"
    og_image = absolute_url(site_url, img)

    return {
        "og_title": og_title,
        "og_description": og_description,
        "og_image": og_image,
        "og_url": canonical,
    }


@router.get("/posts/{slug}", response_model=PostDetailResponse)
async def get_post(slug: str, blog: BlogService = Depends(get_blog_service)):
    post = blog.get_post(slug)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostDetailResponse(
        slug=post.slug,
        title=post.title,
        date=post.date,
        tags=list(post.tags),
        cover_image_url=post.cover_image_url,
        extra_image_urls=list(getattr(post, "extra_image_urls", [])),
        content_html=post.content_html,
    )
