from __future__ import annotations

from datetime import date as Date
from datetime import datetime
from pathlib import Path

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository


def test_filesystem_repository_reads_frontmatter(tmp_path: Path):
    (tmp_path / "hello.md").write_text(
        "---\n"
        "title: Hello\n"
        "date: 2024-01-01\n"
        "tags: [python]\n"
        "emoji: \"🧪\"\n"
        "image: /static/images/hello.png\n"
        "thumb_image: /static/images/hello-thumb.png\n"
        "---\n"
        "Hi there\n",
        encoding="utf-8",
    )

    repo = FilesystemPostsRepository(posts_dir=tmp_path)
    post = repo.get_post("hello")

    assert post is not None
    assert post.title == "Hello"
    assert post.date == "2024-01-01 12:00"
    assert list(post.tags) == ["python"]
    assert post.emoji == "🧪"
    assert post.image == "/static/images/hello.png"
    assert post.thumb_image == "/static/images/hello-thumb.png"


def test_filesystem_repository_normalizes_string_tags_and_infers_blog_tag_for_blog_slug(
    tmp_path: Path,
):
    # Simulate the common mistake: YAML string instead of list.
    # Without normalization, iterating it would produce per-character tags.
    (tmp_path / "blog99.md").write_text(
        "---\n"
        "title: Blog\n"
        "date: 2024-01-01\n"
        "tags: stellody\n"
        "---\n"
        "Body\n",
        encoding="utf-8",
    )

    repo = FilesystemPostsRepository(posts_dir=tmp_path)
    post = repo.get_post("blog99")
    assert post is not None

    # Normalized tags should include the scalar tag.
    assert "stellody" in list(post.tags)
    # And blog slugs should always include the blog category tag.
    assert "cat:blog" in [t.lower() for t in post.tags]


def test_filesystem_repository_normalizes_blank_blurb_and_one_liner_to_none(tmp_path: Path):
    (tmp_path / "hello.md").write_text(
        "---\n"
        "title: Hello\n"
        "date: 2024-01-01 00:00\n"
        "tags: []\n"
        "blurb: \"   \"\n"
        "one_liner: \"\"\n"
        "---\n"
        "Body\n",
        encoding="utf-8",
    )

    repo = FilesystemPostsRepository(posts_dir=tmp_path)
    post = repo.get_post("hello")
    assert post is not None
    assert post.blurb is None
    assert post.one_liner is None


def test_filesystem_repository_handles_none_tags_and_none_extra_images(tmp_path: Path):
    # YAML `null` is valid and should be treated like an empty list.
    (tmp_path / "hello.md").write_text(
        "---\n"
        "title: Hello\n"
        "date: 2024-01-01\n"
        "tags: null\n"
        "extra_images: null\n"
        "---\n"
        "Body\n",
        encoding="utf-8",
    )

    repo = FilesystemPostsRepository(posts_dir=tmp_path)
    post = repo.get_post("hello")
    assert post is not None
    assert list(post.tags) == []
    assert list(post.extra_images) == []


def test_normalize_tags_covers_edge_branches():
    # Empty string should normalize to empty.
    assert FilesystemPostsRepository._normalize_tags("   ") == []

    # Lists can contain None and blank-ish values; those should be skipped.
    assert FilesystemPostsRepository._normalize_tags([None, " blog ", "", "  "]) == ["blog"]

    # Fallback coercion for non-string and non-sequence values.
    assert FilesystemPostsRepository._normalize_tags(123) == ["123"]

    class _WhitespaceStr:
        def __str__(self) -> str:
            return "   "

    # Fallback coercion with a whitespace-only __str__ should normalize to empty.
    assert FilesystemPostsRepository._normalize_tags(_WhitespaceStr()) == []


def test_normalize_published_at_supports_datetime_date_datetime_string_and_fallbacks():
    # datetime passthrough
    dt = datetime(2024, 1, 2, 3, 4)
    assert FilesystemPostsRepository._normalize_published_at(dt) == "2024-01-02 03:04"

    # date -> assumed midday
    d = Date(2024, 1, 2)
    assert FilesystemPostsRepository._normalize_published_at(d) == "2024-01-02 12:00"

    # date-only string -> assumed midday
    assert (
        FilesystemPostsRepository._normalize_published_at("2024-01-02")
        == "2024-01-02 12:00"
    )

    # datetime string with space separator
    assert (
        FilesystemPostsRepository._normalize_published_at("2024-01-02 03:04")
        == "2024-01-02 03:04"
    )

    # invalid string -> ValueError fallback to string coercion
    assert FilesystemPostsRepository._normalize_published_at("not-a-date") == "not-a-date"

    # unknown type -> sentinel default
    assert (
        FilesystemPostsRepository._normalize_published_at(object())
        == "1900-01-01 12:00"
    )
