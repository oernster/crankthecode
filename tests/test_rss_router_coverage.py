from __future__ import annotations

import xml.etree.ElementTree as ET

from fastapi.testclient import TestClient

from app.http.deps import get_blog_service
from app.http.routers import rss as rss_module
from app.main import create_app


def test_rss_helpers_cover_edge_cases():
    # Covers the ValueError/continue path in [`rss._rfc822_date()`](app/http/routers/rss.py:62)
    assert rss_module._rfc822_date("not-a-date") == "not-a-date"

    assert rss_module._first_image_src("<p>No images</p>") is None
    assert (
        rss_module._first_image_src('<img alt="" src="/static/x.png" />')
        == "/static/x.png"
    )

    assert rss_module._absolute_url("https://example.com/", "https://a/b") == "https://a/b"
    assert (
        rss_module._absolute_url("https://example.com/", "/path")
        == "https://example.com/path"
    )

    assert rss_module._guess_image_mime("/a.png") == "image/png"
    assert rss_module._guess_image_mime("/a.jpg") == "image/jpeg"
    assert rss_module._guess_image_mime("/a.jpeg") == "image/jpeg"
    assert rss_module._guess_image_mime("/a.gif") == "image/gif"
    assert rss_module._guess_image_mime("/a.webp") == "image/webp"
    assert rss_module._guess_image_mime("/a.svg") == "image/svg+xml"
    assert rss_module._guess_image_mime("/a.unknown") is None

    wrapped = rss_module._wrap_cdata("hi ]]> bye")
    assert "<![CDATA[" in wrapped
    assert "]]><![CDATA[>" in wrapped


def test_rss_feed_covers_detail_none_and_mime_none_and_mime_present_branches():
    class _Summary:
        def __init__(
            self,
            *,
            slug: str,
            title: str = "T",
            date: str = "2024-01-01 12:00",
            summary_html: str = "<p>S</p>",
        ):
            self.slug = slug
            self.title = title
            self.date = date
            self.summary_html = summary_html

    class _Detail:
        def __init__(
            self,
            *,
            slug: str,
            title: str = "T",
            cover_image_url: str | None,
            content_html: str,
        ):
            self.slug = slug
            self.title = title
            self.cover_image_url = cover_image_url
            self.content_html = content_html

    class _FakeBlog:
        def list_posts(self):
            # - `with-detail-mime`: cover image .png -> mime present -> enclosure branch.
            # - `with-detail-no-mime`: cover image unknown ext -> mime None.
            # - `no-detail`: `get_post` returns None -> description+continue branch.
            return (
                _Summary(slug="with-detail-mime", title="With detail + mime"),
                _Summary(slug="with-detail-no-mime", title="With detail + no mime"),
                _Summary(slug="no-detail", title="No detail"),
            )

        def get_post(self, slug: str):
            if slug == "with-detail-mime":
                return _Detail(
                    slug=slug,
                    title="With detail + mime",
                    cover_image_url="/static/images/x.png",
                    content_html='<p>Body</p><img src="/static/images/inline.png" />',
                )
            if slug == "with-detail-no-mime":
                return _Detail(
                    slug=slug,
                    title="With detail + no mime",
                    cover_image_url="/static/images/x.unknown",
                    content_html="<p>Body</p>",
                )
            return None

    app = create_app()
    app.dependency_overrides[get_blog_service] = lambda: _FakeBlog()
    client = TestClient(app)

    resp = client.get("/rss.xml")
    assert resp.status_code == 200

    # The output includes real CDATA sections after post-processing.
    assert "<![CDATA[" in resp.text

    root = ET.fromstring(resp.content)
    channel = root.find("channel")
    assert channel is not None
    items = channel.findall("item")
    assert len(items) == 3

    media_ns = "http://search.yahoo.com/mrss/"
    content_ns = "http://purl.org/rss/1.0/modules/content/"

    def _link_endswith(item: ET.Element, suffix: str) -> bool:
        link_elem = item.find("link")
        if link_elem is None or link_elem.text is None:
            return False
        return link_elem.text.endswith(suffix)

    # One item should contain media RSS content and an enclosure (mime present).
    mime_item = next(i for i in items if _link_endswith(i, "with-detail-mime"))
    media_content = mime_item.find(f"{{{media_ns}}}content")
    assert media_content is not None
    assert media_content.attrib.get("type") == "image/png"
    enclosure = mime_item.find("enclosure")
    assert enclosure is not None
    assert enclosure.attrib.get("type") == "image/png"

    # One item should include media RSS content but no enclosure (mime None).
    no_mime_item = next(i for i in items if _link_endswith(i, "with-detail-no-mime"))
    media_content_2 = no_mime_item.find(f"{{{media_ns}}}content")
    assert media_content_2 is not None
    assert "type" not in media_content_2.attrib
    assert no_mime_item.find("enclosure") is None

    # The no-detail item should not include content:encoded (we continue early).
    no_detail_item = next(i for i in items if _link_endswith(i, "no-detail"))
    assert no_detail_item.find(f"{{{content_ns}}}encoded") is None

