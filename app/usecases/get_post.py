from __future__ import annotations

from dataclasses import dataclass

from app.usecases.list_posts import _extract_cover_image_and_strip, _strip_image_paragraph

from app.domain.models import PostDetail
from app.ports.markdown_renderer import MarkdownRenderer
from app.ports.posts_repository import PostsRepository


@dataclass(frozen=True, slots=True)
class GetPostUseCase:
    repo: PostsRepository
    renderer: MarkdownRenderer

    def execute(self, slug: str) -> PostDetail | None:
        post = self.repo.get_post(slug)
        if post is None:
            return None

        cover_url = getattr(post, "image", None)
        extra_urls = tuple(getattr(post, "extra_images", ()))
        markdown_wo_cover = post.content_markdown
        if cover_url:
            markdown_wo_cover = _strip_image_paragraph(markdown_wo_cover, cover_url)
        else:
            cover_url, markdown_wo_cover = _extract_cover_image_and_strip(
                post.content_markdown
            )

        for extra_url in extra_urls:
            markdown_wo_cover = _strip_image_paragraph(markdown_wo_cover, extra_url)

        html_content = self.renderer.render(markdown_wo_cover)
        return PostDetail(
            slug=post.slug,
            title=post.title,
            date=post.date,
            tags=post.tags,
            blurb=getattr(post, "blurb", None),
            cover_image_url=cover_url,
            extra_image_urls=extra_urls,
            content_html=html_content,
        )
