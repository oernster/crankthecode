from __future__ import annotations

from dataclasses import dataclass

import re

from app.usecases.list_posts import _extract_cover_image_and_strip, _strip_image_paragraph

from app.domain.models import PostDetail
from app.ports.markdown_renderer import MarkdownRenderer
from app.ports.posts_repository import PostsRepository


_HEADING_RE = re.compile(r"^\s*(?P<hashes>#{1,6})\s+(?P<title>.*?)\s*$")


def _extract_markdown_sections(
    markdown_text: str,
    *,
    title: str,
) -> tuple[str, list[str]]:
    """Extract sections with heading `title` and return (remaining, section_bodies).

    - Matches headings like `## Screenshots` (any level 1-6) case-insensitively.
    - A section runs until the next heading of the same or higher level.
    - Returns only the section *bodies* (excluding the heading line).
    """

    if not markdown_text.strip():
        return markdown_text, []

    lines = markdown_text.splitlines()
    out: list[str] = []
    bodies: list[str] = []
    i = 0
    n = len(lines)
    title_norm = title.strip().lower()

    while i < n:
        m = _HEADING_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue

        heading_title = (m.group("title") or "").strip().lower()
        if heading_title != title_norm:
            out.append(lines[i])
            i += 1
            continue

        level = len(m.group("hashes"))
        i += 1
        body_start = i
        while i < n:
            next_heading = _HEADING_RE.match(lines[i])
            if next_heading and len(next_heading.group("hashes")) <= level:
                break
            i += 1

        body_lines = lines[body_start:i]
        body_text = "\n".join(body_lines).strip()
        if body_text:
            bodies.append(body_text)

    return "\n".join(out).strip(), bodies


def _insert_screenshots_after_problem_solution_impact(
    markdown_text: str,
    *,
    screenshots_markdown: str,
) -> str:
    """Insert `screenshots_markdown` immediately after the Problem→Solution→Impact section.

    If the section isn't found, fall back to appending at the end.
    """

    screenshots_markdown = (screenshots_markdown or "").strip()
    if not screenshots_markdown:
        return markdown_text

    if not markdown_text.strip():
        return f"{screenshots_markdown}\n"

    lines = markdown_text.splitlines()

    # Accept both → and -> variants.
    psi_title_re = re.compile(
        r"^problem\s*(?:→|->)\s*solution\s*(?:→|->)\s*impact$",
        re.IGNORECASE,
    )

    i = 0
    n = len(lines)
    while i < n:
        m = _HEADING_RE.match(lines[i])
        if not m:
            i += 1
            continue

        heading_title = (m.group("title") or "").strip()
        if not psi_title_re.match(heading_title):
            i += 1
            continue

        level = len(m.group("hashes"))
        i += 1
        while i < n:
            next_heading = _HEADING_RE.match(lines[i])
            if next_heading and len(next_heading.group("hashes")) <= level:
                break
            i += 1

        insert_at = i
        new_lines = lines[:insert_at] + [""] + screenshots_markdown.splitlines() + [""] + lines[insert_at:]
        return "\n".join(new_lines).strip() + "\n"

    # Fallback: append.
    return markdown_text.strip() + "\n\n" + screenshots_markdown + "\n"


def _axisdb_install_prompt_markdown() -> str:
    """AxisDB: HTML block injected after the Problem→Solution→Impact section."""

    return """<div class=\"fake-terminal fake-terminal--axisdb-install\" aria-label=\"Install AxisDB\">
  <div class=\"fake-terminal__title\">
    <span>bash</span>
    <button
      class=\"code-copy code-copy--icon\"
      type=\"button\"
      data-copy-target=\"axisdb-install-commands\"
      aria-label=\"Copy install commands\"
      title=\"Copy install commands\"
    >
      <svg class=\"code-copy__icon\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\">
        <path
          d=\"M16 1H6a2 2 0 0 0-2 2v12h2V3h10V1Zm3 4H10a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Zm0 16H10V7h9v14Z\"
        />
      </svg>
    </button>
  </div>
  <pre class=\"fake-terminal__body\"><code><span class=\"ft-step ft-step--1\"><span class=\"fake-terminal__prompt\">user@linux:~$ </span><span class=\"fake-terminal__typed fake-terminal__typed--1\">python3 -m venv venv</span><span class=\"fake-terminal__cursor-wrap fake-terminal__cursor-wrap--1\" aria-hidden=\"true\"><span class=\"fake-terminal__cursor\"></span></span></span>
<span class=\"ft-step ft-step--2\"><span class=\"fake-terminal__prompt\">user@linux:~$ </span><span class=\"fake-terminal__typed fake-terminal__typed--2\">source venv/bin/activate</span><span class=\"fake-terminal__cursor-wrap fake-terminal__cursor-wrap--2\" aria-hidden=\"true\"><span class=\"fake-terminal__cursor\"></span></span></span>
<span class=\"ft-step ft-step--3\"><span class=\"fake-terminal__prompt\">user@linux:~$ </span><span class=\"fake-terminal__typed fake-terminal__typed--3\">pip install --upgrade pip</span><span class=\"fake-terminal__cursor-wrap fake-terminal__cursor-wrap--3\" aria-hidden=\"true\"><span class=\"fake-terminal__cursor\"></span></span></span>
<span class=\"ft-step ft-step--4\"><span class=\"fake-terminal__prompt\">user@linux:~$ </span><span class=\"fake-terminal__typed fake-terminal__typed--4\">pip install axisdb</span><span class=\"fake-terminal__cursor-wrap fake-terminal__cursor-wrap--4\" aria-hidden=\"true\"><span class=\"fake-terminal__cursor\"></span></span></span></code></pre>

  <pre class=\"visually-hidden\"><code id=\"axisdb-install-commands\">python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install axisdb</code></pre>
</div>"""


def _has_problem_solution_impact_section(markdown_text: str) -> bool:
    """Return True if markdown contains a Problem→Solution→Impact heading."""

    if not markdown_text.strip():
        return False

    psi_title_re = re.compile(
        r"^problem\s*(?:→|->)\s*solution\s*(?:→|->)\s*impact$",
        re.IGNORECASE,
    )
    for line in markdown_text.splitlines():
        m = _HEADING_RE.match(line)
        if not m:
            continue
        title = (m.group("title") or "").strip()
        if psi_title_re.match(title):
            return True
    return False


@dataclass(frozen=True, slots=True)
class GetPostUseCase:
    repo: PostsRepository
    renderer: MarkdownRenderer

    def execute(self, slug: str) -> PostDetail | None:
        post = self.repo.get_post(slug)
        if post is None:
            return None

        cover_url = getattr(post, "image", None)
        social_url = getattr(post, "social_image", None)
        extra_urls = tuple(getattr(post, "extra_images", ()))

        # Start from raw markdown.
        markdown_wo_cover = post.content_markdown

        # 1) Strip explicit cover image paragraph (if present) *near the start*.
        if cover_url:
            markdown_wo_cover = _strip_image_paragraph(
                markdown_wo_cover,
                cover_url,
                head=2,
            )

        # 2) Extract author-provided Screenshots section *before* cover extraction.
        # This prevents an image inside "## Screenshots" from being mis-detected as
        # the cover when `image:` is not set in frontmatter.
        markdown_wo_cover, embedded_screenshots_bodies = _extract_markdown_sections(
            markdown_wo_cover,
            title="Screenshots",
        )

        # 3) If no explicit cover image, derive it from the remaining markdown.
        if not cover_url:
            cover_url, markdown_wo_cover = _extract_cover_image_and_strip(
                markdown_wo_cover
            )

        # 4) `extra_images` are rendered in a controlled place.
        # If the author embedded them as standalone image paragraphs, strip them to
        # avoid duplication.
        for extra_url in extra_urls:
            markdown_wo_cover = _strip_image_paragraph(markdown_wo_cover, extra_url)

        has_psi = _has_problem_solution_impact_section(markdown_wo_cover)

        # AxisDB flourish: inject the install prompt immediately after PSI.
        # (This is intentionally independent of the screenshots placement.)
        if has_psi and (post.slug or "").strip().lower() == "axisdb":
            markdown_wo_cover = _insert_screenshots_after_problem_solution_impact(
                markdown_wo_cover,
                screenshots_markdown=_axisdb_install_prompt_markdown(),
            )

        # Always render `extra_images` in a controlled place: append a Screenshots
        # section at the end (plus any author-provided Screenshots section bodies).
        screenshot_urls: list[str] = []
        seen: set[str] = set()
        for url in extra_urls:
            if not url:
                continue
            if url in seen:
                continue
            seen.add(url)
            screenshot_urls.append(url)

        screenshots_parts: list[str] = []
        if screenshot_urls or embedded_screenshots_bodies:
            screenshots_parts.append("## Screenshots")
            for url in screenshot_urls:
                screenshots_parts.append(f"![{post.title}]({url})")
                screenshots_parts.append("")
            for body in embedded_screenshots_bodies:
                screenshots_parts.append(body.strip())
                screenshots_parts.append("")

        screenshots_md = "\n".join(screenshots_parts).strip()
        if screenshots_md:
            if markdown_wo_cover.strip():
                markdown_wo_cover = markdown_wo_cover.strip() + "\n\n" + screenshots_md + "\n"
            else:
                markdown_wo_cover = screenshots_md + "\n"

        html_content = self.renderer.render(markdown_wo_cover)
        return PostDetail(
            slug=post.slug,
            title=post.title,
            date=post.date,
            tags=post.tags,
            blurb=getattr(post, "blurb", None),
            one_liner=getattr(post, "one_liner", None),
            cover_image_url=cover_url,
            social_image_url=social_url,
            extra_image_urls=extra_urls,
            content_html=html_content,
            emoji=getattr(post, "emoji", None),
        )
