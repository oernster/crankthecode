from __future__ import annotations

import asyncio
import json
import os
from types import SimpleNamespace

from app.http.routers import mmsp as mmsp_module
from app.http.routers.mmsp import mmsp_feed


class _FakeRequest:
    base_url = "https://example.com/"


class _Post:
    def __init__(
        self,
        *,
        slug: str = "my-post",
        title: str = "My Post",
        date: str = "2025-01-15",
        blurb: str | None = "A blurb",
        one_liner: str | None = None,
        cover_image_url: str | None = None,
        tags: list | None = None,
    ):
        self.slug = slug
        self.title = title
        self.date = date
        self.blurb = blurb
        self.one_liner = one_liner
        self.cover_image_url = cover_image_url
        self.tags = tags if tags is not None else []


class _Blog:
    def __init__(self, posts):
        self._posts = posts

    def list_posts(self):
        return self._posts


def _run(posts):
    os.environ["SITE_URL"] = "https://example.com/"
    try:
        return asyncio.run(mmsp_feed(_FakeRequest(), _Blog(posts)))
    finally:
        os.environ.pop("SITE_URL", None)


def test_to_iso_utc_datetime_format():
    result = mmsp_module._to_iso_utc("2025-04-10 14:30")
    assert result == "2025-04-10T14:30:00+00:00"


def test_to_iso_utc_date_only_defaults_to_noon():
    result = mmsp_module._to_iso_utc("2025-04-10")
    assert result == "2025-04-10T12:00:00+00:00"


def test_to_iso_utc_empty_returns_none():
    assert mmsp_module._to_iso_utc("") is None


def test_to_iso_utc_invalid_returns_none():
    assert mmsp_module._to_iso_utc("not-a-date") is None


def test_absolute_passes_through_https():
    result = mmsp_module._absolute("https://example.com/", "https://cdn.example.com/img.png")
    assert result == "https://cdn.example.com/img.png"


def test_absolute_resolves_relative_path():
    result = mmsp_module._absolute("https://example.com/", "/static/img.png")
    assert result == "https://example.com/static/img.png"


def test_is_excluded_hidden_slugs():
    for slug in ("about-me", "start-here", "portfolio"):
        post = SimpleNamespace(slug=slug, tags=[])
        assert mmsp_module._is_excluded(post) is True


def test_is_excluded_leadership_tag():
    post = SimpleNamespace(slug="some-post", tags=["cat:leadership", "python"])
    assert mmsp_module._is_excluded(post) is True


def test_is_excluded_normal_post():
    post = SimpleNamespace(slug="my-project", tags=["python", "tools"])
    assert mmsp_module._is_excluded(post) is False


def test_is_excluded_no_tags():
    post = SimpleNamespace(slug="hello", tags=[])
    assert mmsp_module._is_excluded(post) is False


def test_is_excluded_none_tags():
    post = SimpleNamespace(slug="hello", tags=None)
    assert mmsp_module._is_excluded(post) is False


def test_is_excluded_uppercase_hidden_slug():
    post = SimpleNamespace(slug="ABOUT-ME", tags=[])
    assert mmsp_module._is_excluded(post) is True


def test_is_excluded_mixed_case_leadership_tag():
    post = SimpleNamespace(slug="post", tags=["CAT:LEADERSHIP"])
    assert mmsp_module._is_excluded(post) is True


def test_is_excluded_non_iterable_tags_returns_false():
    post = SimpleNamespace(slug="post", tags=42)
    assert mmsp_module._is_excluded(post) is False


def test_mmsp_feed_handler_manifest_structure():
    resp = _run([_Post()])
    body = json.loads(resp.body)

    assert body["mmsp"] == "1.0"
    assert body["feed_url"] == "https://example.com/.well-known/mmsp.json"
    assert body["id"] == body["feed_url"]
    assert body["title"] == "Crank The Code"
    assert body["language"] == "en"
    assert body["authors"][0]["name"] == "Oliver Ernster"
    assert body["poll"]["min"] == 300
    assert body["poll"]["recommended"] == 3600
    assert "application/mmsp+json" in resp.media_type


def test_mmsp_feed_handler_item_with_blurb_and_no_cover():
    resp = _run([_Post(blurb="My blurb", cover_image_url=None, tags=["python"])])
    items = json.loads(resp.body)["items"]

    assert len(items) == 1
    item = items[0]
    assert item["type"] == "article"
    assert item["description"] == "My blurb"
    assert "thumbnail" not in item
    assert item["tags"] == ["python"]


def test_mmsp_feed_handler_item_with_cover_and_no_blurb():
    resp = _run([_Post(blurb=None, one_liner=None, cover_image_url="/static/x.png", tags=[])])
    items = json.loads(resp.body)["items"]

    item = items[0]
    assert "description" not in item
    assert item["thumbnail"][0]["url"] == "https://example.com/static/x.png"
    assert "tags" not in item


def test_mmsp_feed_handler_item_one_liner_fallback():
    resp = _run([_Post(blurb=None, one_liner="Short line")])
    items = json.loads(resp.body)["items"]

    assert items[0]["description"] == "Short line"


def test_mmsp_feed_handler_skips_post_with_bad_date():
    posts = [
        _Post(slug="good", date="2025-01-01"),
        _Post(slug="bad", date="not-a-date"),
    ]
    items = json.loads(_run(posts).body)["items"]

    slugs = [i["url"].split("/")[-1] for i in items]
    assert "good" in slugs
    assert "bad" not in slugs


def test_mmsp_feed_handler_strips_cat_prefix_tags():
    resp = _run([_Post(tags=["cat:blog", "python", "cat:tools", "software"])])
    items = json.loads(resp.body)["items"]

    assert items[0]["tags"] == ["python", "software"]


def test_mmsp_feed_handler_item_url_is_absolute():
    resp = _run([_Post(slug="hello-world")])
    items = json.loads(resp.body)["items"]

    assert items[0]["url"] == "https://example.com/posts/hello-world"
    assert items[0]["id"] == "https://example.com/posts/hello-world#mmsp-v1"


def test_mmsp_feed_handler_excludes_hidden_posts():
    posts = [
        _Post(slug="about-me"),
        _Post(slug="real-post"),
        _Post(slug="start-here"),
    ]
    items = json.loads(_run(posts).body)["items"]

    slugs = [i["url"].split("/")[-1] for i in items]
    assert "about-me" not in slugs
    assert "start-here" not in slugs
    assert "real-post" in slugs


def test_mmsp_feed_handler_caps_at_twenty_items():
    posts = [_Post(slug=f"post-{i}") for i in range(30)]
    items = json.loads(_run(posts).body)["items"]

    assert len(items) == 20


def test_mmsp_feed_handler_empty_posts():
    items = json.loads(_run([]).body)["items"]
    assert items == []
