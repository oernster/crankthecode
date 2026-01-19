from __future__ import annotations

from pathlib import Path

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository


def test_filesystem_repository_reads_frontmatter(tmp_path: Path):
    (tmp_path / "hello.md").write_text(
        "---\n"
        "title: Hello\n"
        "date: 2024-01-01\n"
        "tags: [python]\n"
        "---\n"
        "Hi there\n",
        encoding="utf-8",
    )

    repo = FilesystemPostsRepository(posts_dir=tmp_path)
    post = repo.get_post("hello")

    assert post is not None
    assert post.title == "Hello"
    assert post.date == "2024-01-01"
    assert list(post.tags) == ["python"]
