from __future__ import annotations

from pathlib import Path

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository


def test_filesystem_repository_reads_frontmatter(tmp_path: Path):
    (tmp_path / "hello.md").write_text(
        "---\n"
        "title: Hello\n"
        "date: 2024-01-01\n"
        "tags: [python]\n"
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
    assert post.image == "/static/images/hello.png"
    assert post.thumb_image == "/static/images/hello-thumb.png"


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
