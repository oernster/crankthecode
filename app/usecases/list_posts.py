from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import re

from app.domain.models import PostSummary
from app.ports.markdown_renderer import MarkdownRenderer
from app.ports.posts_repository import PostsRepository


def _extract_summary_markdown(markdown_text: str) -> str:
    """Extract a summary as the first paragraph.

    Mirrors the original behavior: split on a blank line and use the first chunk.
    """

    parts = markdown_text.split("\n\n", 1)
    return parts[0].strip()


_COVER_IMAGE_PARAGRAPH_RE = re.compile(
    r"^!\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)\s*$"
)

def _extract_cover_image_and_strip(markdown_text: str) -> tuple[str | None, str]:
    """Extract a cover image and remove it from the rendered markdown.

    Rule:
    - the *first standalone image paragraph anywhere* in the post is treated as
      the cover, e.g. `![Alt](/static/images/cover.jpg)`.
    - that paragraph is removed from the content so the image doesn't show up
      again in the post body.

    This lets you put the cover image at the top or bottom of the markdown
    without duplication.
    """

    paragraphs = [p.strip() for p in markdown_text.split("\n\n")]
    # Keep empty paragraphs out; we'll re-join with a single blank line.
    paragraphs = [p for p in paragraphs if p]
    if not paragraphs:
        return None, markdown_text

    for idx, para in enumerate(paragraphs):
        match = _COVER_IMAGE_PARAGRAPH_RE.match(para)
        if match:
            cover_url = match.group(1)
            remaining = (paragraphs[:idx] + paragraphs[idx + 1 :])
            return cover_url, "\n\n".join(remaining).strip()

    return None, markdown_text


def _strip_image_paragraph(
    markdown_text: str,
    image_url: str,
    *,
    head: int | None = None,
    tail: int | None = None,
) -> str:
    """Remove a standalone image paragraph that points to `image_url`.

    By default this removes the first matching paragraph anywhere.

    When `head` and/or `tail` are provided, removal is restricted to paragraphs
    near the start and/or end of the document. This matches the intended
    "cover image" use-case where authors typically place the cover at the top
    or bottom of the post, while still allowing the same image to appear later
    in the body (e.g. in a screenshots section).
    """

    paragraphs = [p.strip() for p in markdown_text.split("\n\n")]
    paragraphs = [p for p in paragraphs if p]
    if not paragraphs:
        return markdown_text

    candidate_indices: list[int]
    if head is None and tail is None:
        candidate_indices = list(range(len(paragraphs)))
    else:
        n = len(paragraphs)
        indices: set[int] = set()
        if head and head > 0:
            indices.update(range(min(head, n)))
        if tail and tail > 0:
            indices.update(range(max(0, n - tail), n))
        candidate_indices = sorted(indices)

    for idx in candidate_indices:
        para = paragraphs[idx]
        match = _COVER_IMAGE_PARAGRAPH_RE.match(para)
        if match and match.group(1) == image_url:
            remaining = (paragraphs[:idx] + paragraphs[idx + 1 :])
            return "\n\n".join(remaining).strip()

    return markdown_text


@dataclass(frozen=True, slots=True)
class ListPostsUseCase:
    repo: PostsRepository
    renderer: MarkdownRenderer

    def execute(self) -> Sequence[PostSummary]:
        posts = []
        for post in self.repo.list_posts():
            cover_url = getattr(post, "image", None)
            thumb_url = getattr(post, "thumb_image", None)
            markdown_wo_cover = post.content_markdown
            if cover_url:
                # Only strip the cover when the author placed it near the start/end.
                # This avoids surprising removals when the same image is later used
                # in the body (e.g. in a screenshots section).
                markdown_wo_cover = _strip_image_paragraph(
                    markdown_wo_cover,
                    cover_url,
                    # Only strip when the image is very near the start (first or
                    # second paragraph). This preserves legitimate reuse later
                    # (e.g. screenshots section).
                    head=2,
                )
            else:
                cover_url, markdown_wo_cover = _extract_cover_image_and_strip(
                    post.content_markdown
                )

            # Prefer explicit thumb image for list tiles/buttons; fall back to cover.
            if not thumb_url:
                thumb_url = cover_url

            # Also strip any `extra_images` (if present) so they don't appear twice
            # (once in the custom gallery and again if the author embedded them).
            for extra_url in getattr(post, "extra_images", ()):
                markdown_wo_cover = _strip_image_paragraph(markdown_wo_cover, extra_url)

            markdown_for_summary = markdown_wo_cover
            summary_md = _extract_summary_markdown(markdown_for_summary)
            summary_html = self.renderer.render(summary_md)
            posts.append(
                PostSummary(
                    slug=post.slug,
                    title=post.title,
                    date=post.date,
                    tags=post.tags,
                    blurb=getattr(post, "blurb", None),
                    one_liner=getattr(post, "one_liner", None),
                    cover_image_url=cover_url,
                    thumb_image_url=thumb_url,
                    emoji=getattr(post, "emoji", None),
                    summary_html=summary_html,
                )
            )

        # Keep original semantics: string-sort date descending (YYYY-MM-DD expected)
        return tuple(sorted(posts, key=lambda p: p.date, reverse=True))
