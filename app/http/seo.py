from __future__ import annotations

import os
import re
from datetime import datetime
from urllib.parse import urljoin

from fastapi import Request


DEFAULT_SITE_URL = "https://www.crankthecode.com/"


_WS_RE = re.compile(r"\s+")


def get_site_url(request: Request | None = None) -> str:
    """Return the canonical site base URL (always trailing slash).

    Priority:
    1) `SITE_URL` environment variable
    2) `request.base_url` when provided
    3) project default
    """

    configured = (os.getenv("SITE_URL") or "").strip()
    if configured:
        return configured.rstrip("/") + "/"

    if request is not None:
        return str(request.base_url).rstrip("/") + "/"

    return DEFAULT_SITE_URL


def absolute_url(site_url: str, url_or_path: str) -> str:
    """Build an absolute URL from a site base and a URL/path."""

    return urljoin(site_url, url_or_path)


def canonical_url_for_request(request: Request, site_url: str) -> str:
    """Canonical URL for the current request.

    We preserve the query string (useful for category pages like /posts?q=python).
    """

    path = request.url.path
    query = str(request.url.query or "").strip()
    base = site_url.rstrip("/")
    return f"{base}{path}" + (f"?{query}" if query else "")


def build_meta_description(
    primary: str | None,
    *,
    fallback: str | None = None,
    default: str = "",
    max_len: int = 160,
) -> str:
    """Return a compact meta description.

    Assumes `primary`/`fallback` are already plain text (frontmatter). We still
    normalize whitespace and clamp length.
    """

    raw = (primary or fallback or default or "").strip()
    if not raw:
        return ""
    compact = _WS_RE.sub(" ", raw)
    if len(compact) <= max_len:
        return compact
    return compact[: max_len - 1].rstrip() + "…"


def to_iso_date(value: str) -> str | None:
    """Parse known post date formats into an ISO-8601 date string.

    Supported inputs:
    - "YYYY-MM-DD HH:MM" (current post storage)
    - "YYYY-MM-DD"
    """

    raw = (value or "").strip()
    if not raw:
        return None

    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(raw, fmt)
            return dt.date().isoformat()
        except ValueError:
            continue
    return None


def to_iso_datetime(value: str) -> str | None:
    """Parse known post date formats into an ISO-8601 datetime string.

    Supported inputs:
    - "YYYY-MM-DD HH:MM" (current post storage)
    - "YYYY-MM-DD" (assumed 12:00)

    Returns a naive ISO datetime like "2026-01-20T10:10:00".
    """

    raw = (value or "").strip()
    if not raw:
        return None

    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(raw, fmt)
            if fmt == "%Y-%m-%d":
                dt = dt.replace(hour=12, minute=0, second=0, microsecond=0)
            else:
                dt = dt.replace(second=0, microsecond=0)
            return dt.isoformat()
        except ValueError:
            continue

    return None

