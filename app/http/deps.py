from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import Request

from app.adapters.filesystem_posts_repository import FilesystemPostsRepository
from app.adapters.markdown_python_renderer import PythonMarkdownRenderer
from app.services.blog_service import BlogService
from app.usecases.get_post import GetPostUseCase
from app.usecases.list_posts import ListPostsUseCase


@lru_cache(maxsize=1)
def _posts_repo() -> FilesystemPostsRepository:
    return FilesystemPostsRepository(posts_dir=Path("posts"))


@lru_cache(maxsize=1)
def _markdown_renderer() -> PythonMarkdownRenderer:
    return PythonMarkdownRenderer()


def get_blog_service() -> BlogService:
    repo = _posts_repo()
    renderer = _markdown_renderer()
    return BlogService(
        list_posts_uc=ListPostsUseCase(repo=repo, renderer=renderer),
        get_post_uc=GetPostUseCase(repo=repo, renderer=renderer),
    )


def get_templates(request: Request):
    return request.app.state.templates
