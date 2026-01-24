from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from app.services.blog_service import BlogService


@dataclass(frozen=True, slots=True)
class _PostSummary:
    slug: str
    title: str
    date: str
    tags: Sequence[str]
    blurb: str | None
    one_liner: str | None
    cover_image_url: str | None
    thumb_image_url: str | None
    summary_html: str


@dataclass(frozen=True, slots=True)
class _PostDetail:
    slug: str
    title: str
    date: str
    tags: Sequence[str]
    blurb: str | None
    one_liner: str | None
    cover_image_url: str | None
    extra_image_urls: Sequence[str]
    content_html: str
    social_image_url: str | None = None


def make_fake_blog_service() -> BlogService:
    # We return an object with the BlogService interface (duck-typing) but also
    # explicitly annotate the return type as BlogService to align with Depends.
    summaries = (
        _PostSummary(
            slug="hello",
            title="Hello",
            date="2024-01-01 12:00",
            tags=("python",),
            blurb="A short blurb",
            one_liner="A one-liner",
            cover_image_url="/static/images/hello.png",
            thumb_image_url="/static/images/hello-thumb.png",
            summary_html="<p>Summary</p>",
        ),
        _PostSummary(
            slug="no-detail",
            title="No Detail",
            date="2024-01-01 12:00",
            tags=(),
            blurb=None,
            one_liner=None,
            cover_image_url=None,
            thumb_image_url=None,
            summary_html="<p>No detail summary</p>",
        ),
    )
    details = {
        "hello": _PostDetail(
            slug="hello",
            title="Hello",
            date="2024-01-01 12:00",
            tags=("python",),
            blurb="A short blurb",
            one_liner="A one-liner",
            cover_image_url="/static/images/hello.png",
            extra_image_urls=("/static/images/extra.png",),
            content_html='<h1>Hello</h1><img src="/static/images/inline.png" />',
            social_image_url=None,
        )
    }

    class _FakeBlog:
        def list_posts(self):
            return summaries

        def get_post(self, slug: str):
            return details.get(slug)

    return _FakeBlog()  # type: ignore[return-value]
