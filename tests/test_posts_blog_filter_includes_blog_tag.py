from __future__ import annotations

from pathlib import Path


def test_posts_blog_view_has_blog_in_data_search_for_blog_slugs(tmp_path: Path):
    """Regression: `/posts?q=blog` deep-link expects `blog` to be in title/tags.

    On `/posts`, filtering is client-side and relies on `data-search`, which is
    generated from `title + tags` in [`templates/posts.html:9`](templates/posts.html:9).

    This test ensures our repository normalizes tags and injects the `blog` tag
    for `blog*` slugs so the deep-link reliably matches.
    """

    (tmp_path / "blog999.md").write_text(
        "---\n"
        "title: Some Blog Post\n"
        "date: 2026-01-01\n"
        # Intentionally omit `blog` here; slug-based inference should add it.
        "tags: [stellody]\n"
        "---\n\n"
        "Body\n",
        encoding="utf-8",
    )

    from fastapi.testclient import TestClient

    from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
    from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
    from app.http.deps import get_blog_service
    from app.main import create_app
    from app.services.blog_service import BlogService
    from app.usecases.get_post import GetPostUseCase
    from app.usecases.list_posts import ListPostsUseCase

    repo = FilesystemPostsRepository(posts_dir=tmp_path)
    renderer = PythonMarkdownRenderer()
    blog = BlogService(
        list_posts_uc=ListPostsUseCase(repo=repo, renderer=renderer),
        get_post_uc=GetPostUseCase(repo=repo, renderer=renderer),
    )

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: blog
    client = TestClient(app)

    resp = client.get("/posts?q=blog")
    assert resp.status_code == 200

    assert "Some Blog Post" in resp.text
    # Ensure `blog` makes it into the `data-search` attribute.
    assert "data-search=\"some blog post blog" in resp.text.lower()
