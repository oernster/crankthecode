"""Tests for _CachePolicyMiddleware branches not covered by integration tests.

Covered here:
- Non-HTTP scope (WebSocket/lifespan) passes through unmodified.
- Dynamic content that already carries Cache-Control is left alone (has_cc branch).
"""
from __future__ import annotations

import pytest

from app.main import _CachePolicyMiddleware


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_send_collector():
    """Returns (send callable, messages list)."""
    messages: list[dict] = []

    async def send(message: dict) -> None:
        messages.append(message)

    return send, messages


def _make_receive():
    async def receive():
        return {}

    return receive


# ---------------------------------------------------------------------------
# Non-HTTP scope passthrough
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_non_http_scope_passes_through_unmodified():
    """Lifespan / WebSocket scopes must not be intercepted."""

    received_scopes: list[dict] = []

    async def inner_app(scope, receive, send):
        received_scopes.append(scope)

    middleware = _CachePolicyMiddleware(inner_app)

    scope = {"type": "lifespan"}
    send, _ = _make_send_collector()

    await middleware(scope, _make_receive(), send)

    assert received_scopes == [scope], "Scope must be forwarded unchanged to inner app"


# ---------------------------------------------------------------------------
# Dynamic content that already has Cache-Control (has_cc=True branch)
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_dynamic_content_with_existing_cache_control_is_unchanged():
    """RSS/XML responses that already carry Cache-Control are left as-is."""

    existing_cc = b"max-age=300"

    start_message = {
        "type": "http.response.start",
        "status": 200,
        "headers": [
            (b"content-type", b"application/rss+xml; charset=utf-8"),
            (b"cache-control", existing_cc),
        ],
    }
    body_message = {"type": "http.response.body", "body": b"<rss/>"}

    async def inner_app(scope, receive, send):
        await send(start_message)
        await send(body_message)

    middleware = _CachePolicyMiddleware(inner_app)
    scope = {"type": "http"}
    send, collected = _make_send_collector()

    await middleware(scope, _make_receive(), send)

    start = collected[0]
    headers = dict(start["headers"])
    # Must NOT have been overwritten — existing value must survive.
    assert headers[b"cache-control"] == existing_cc
