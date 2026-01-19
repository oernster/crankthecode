from __future__ import annotations

import os
import xml.etree.ElementTree as ET

from fastapi.testclient import TestClient

from app.main import create_app


def _get_text(parent: ET.Element, tag: str) -> str | None:
    elem = parent.find(tag)
    if elem is None:
        return None
    return elem.text


def test_rss_endpoint_responds_with_rss2_xml():
    app = create_app()
    client = TestClient(app)

    resp = client.get("/rss.xml")

    assert resp.status_code == 200
    assert "xml" in resp.headers.get("content-type", "").lower()

    root = ET.fromstring(resp.text)
    assert root.tag == "rss"
    assert root.attrib.get("version") == "2.0"
    assert root.find("channel") is not None


def test_rss_items_have_expected_fields_and_absolute_links():
    # Ensure deterministic base URL for absolute links.
    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/rss.xml")
        assert resp.status_code == 200

        root = ET.fromstring(resp.text)
        channel = root.find("channel")
        assert channel is not None

        items = channel.findall("item")
        assert len(items) >= 1
        assert len(items) <= 20

        # Validate the first item contract.
        item = items[0]
        title = _get_text(item, "title")
        link = _get_text(item, "link")
        guid = _get_text(item, "guid")
        description = _get_text(item, "description")
        pub_date = _get_text(item, "pubDate")

        assert title
        assert link and link.startswith("https://example.com/")
        assert guid
        assert guid.startswith(link)
        assert description
        assert pub_date
    finally:
        os.environ.pop("SITE_URL", None)


def test_rss_items_include_media_image_when_post_contains_img_tag():
    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/rss.xml")
        assert resp.status_code == 200

        root = ET.fromstring(resp.text)
        channel = root.find("channel")
        assert channel is not None

        items = channel.findall("item")
        assert len(items) >= 1

        media_ns = "http://search.yahoo.com/mrss/"
        media_tag = f"{{{media_ns}}}content"

        media_elems = [item.find(media_tag) for item in items]
        media_elems = [elem for elem in media_elems if elem is not None]

        # At least one post includes an image in its markdown.
        assert len(media_elems) >= 1
        assert media_elems[0].attrib.get("url", "").startswith("https://example.com/")

        # Thumbnail should also be present for better Feedly support.
        thumb_tag = f"{{{media_ns}}}thumbnail"
        thumbs = [item.find(thumb_tag) for item in items]
        thumbs = [elem for elem in thumbs if elem is not None]
        assert len(thumbs) >= 1
    finally:
        os.environ.pop("SITE_URL", None)


def test_rss_items_include_content_encoded_html_with_leading_img_for_feed_thumbnails():
    """Feed readers like Feedly often derive list thumbnails from item HTML.

    Ensure we provide `content:encoded` containing an <img> at the top.
    """

    os.environ["SITE_URL"] = "https://example.com"
    try:
        app = create_app()
        client = TestClient(app)

        resp = client.get("/rss.xml")
        assert resp.status_code == 200

        root = ET.fromstring(resp.text)
        channel = root.find("channel")
        assert channel is not None

        items = channel.findall("item")
        assert len(items) >= 1

        # Look for at least one content:encoded element containing an <img src="...">.
        content_ns = "http://purl.org/rss/1.0/modules/content/"
        content_tag = f"{{{content_ns}}}encoded"

        encoded = [item.find(content_tag) for item in items]
        encoded = [elem for elem in encoded if elem is not None and elem.text]
        assert len(encoded) >= 1

        encoded_text = encoded[0].text or ""
        assert "<img" in encoded_text
        assert "https://example.com/" in encoded_text
    finally:
        os.environ.pop("SITE_URL", None)

