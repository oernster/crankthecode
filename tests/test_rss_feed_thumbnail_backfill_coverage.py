from __future__ import annotations


import os
import xml.etree.ElementTree as ET
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.http.deps import get_blog_service
from app.main import create_app


def test_rss_thumbnail_backfill_scans_older_posts_and_replaces_last_item():
    """Cover rss_feed() backfill branches.

    Targets missing coverage reported in `app.http.routers.rss` around lines 204-206, 208:
    - find a replacement in eligible_posts[20:200]
    - replace the last of the first 20 posts when replacement found
    """

    os.environ["SITE_URL"] = "https://example.com"
    try:
        # First 20: no images.
        first_20 = [
            SimpleNamespace(
                slug=f"p{i}",
                title=f"P{i}",
                date="2026-01-01 12:00",
                tags=(),
                summary_html="<p>No image</p>",
            )
            for i in range(20)
        ]

        # Candidate window: ensure at least one older post has an image.
        replacement_summary = SimpleNamespace(
            slug="old-with-image",
            title="Old With Image",
            date="2025-12-31 12:00",
            tags=(),
            summary_html='<p><img src="/static/images/x.png" /></p>',
        )

        # Provide some non-image candidates first to force scanning.
        older = [
            SimpleNamespace(
                slug=f"old{i}",
                title=f"Old{i}",
                date="2025-12-01 12:00",
                tags=(),
                summary_html="<p>Still no image</p>",
            )
            for i in range(3)
        ] + [replacement_summary]

        eligible = [*first_20, *older]

        class FakeBlog:
            def list_posts(self):
                return tuple(eligible)

            def get_post(self, slug: str):
                # Detail is required so rss_feed() doesn't hit the early `continue`.
                # Provide a cover so image is picked.
                return SimpleNamespace(
                    slug=slug,
                    title=slug,
                    date="2026-01-01 12:00",
                    tags=(),
                    cover_image_url="/static/images/x.png",
                    content_html="<p>Body</p>",
                )

        app = create_app()
        app.dependency_overrides[get_blog_service] = lambda: FakeBlog()
        client = TestClient(app)

        resp = client.get("/rss.xml")
        assert resp.status_code == 200

        root = ET.fromstring(resp.content)
        channel = root.find("channel")
        assert channel is not None
        items = channel.findall("item")
        assert len(items) == 20

        links = [item.findtext("link") for item in items]
        assert any((link or "").endswith("/posts/old-with-image") for link in links)
    finally:
        os.environ.pop("SITE_URL", None)

