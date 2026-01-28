from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class PostSummaryResponse(BaseModel):
    slug: str
    title: str
    date: str
    tags: List[str] = Field(default_factory=list)
    emoji: str | None = None
    summary_html: str


class PostDetailResponse(BaseModel):
    slug: str
    title: str
    date: str
    tags: List[str] = Field(default_factory=list)
    cover_image_url: str | None = None
    emoji: str | None = None
    extra_image_urls: List[str] = Field(default_factory=list)
    content_html: str
