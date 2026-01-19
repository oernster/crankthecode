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
        assert guid == link
        assert description
        assert pub_date
    finally:
        os.environ.pop("SITE_URL", None)

