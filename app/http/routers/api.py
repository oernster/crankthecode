from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

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
