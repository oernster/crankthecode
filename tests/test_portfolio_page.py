"""The portfolio moved to ernster.dev; /portfolio only redirects there now."""

from __future__ import annotations

from fastapi import status
from fastapi.testclient import TestClient

from app.http.routers.portfolio import PORTFOLIO_HUB_URL
from app.main import create_app


def test_portfolio_redirects_permanently_to_ernster_dev():
    # base_url bypasses the canonical-host middleware so the portfolio
    # route itself answers (localhost is exempt from host canonicalisation).
    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/portfolio", follow_redirects=False)

    assert resp.status_code == status.HTTP_301_MOVED_PERMANENTLY
    assert resp.headers["location"] == PORTFOLIO_HUB_URL
    assert PORTFOLIO_HUB_URL == "https://ernster.dev"


def test_portfolio_redirect_covers_legacy_section_urls():
    """Old /portfolio?section=... deep links must land on the hub too."""

    app = create_app()
    client = TestClient(app, base_url="http://localhost")

    resp = client.get("/portfolio?section=desktop-applications", follow_redirects=False)

    assert resp.status_code == status.HTTP_301_MOVED_PERMANENTLY
    assert resp.headers["location"] == PORTFOLIO_HUB_URL
