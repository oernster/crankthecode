from __future__ import annotations

import re
from typing import Optional

from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.responses import Response


_FINGERPRINT_RE = re.compile(r"\.[0-9a-f]{8,}\.")


class CachingStaticFiles(StaticFiles):
    """StaticFiles with production caching semantics.

    - Fingerprinted assets: cache for 1y immutable.
    - Non-fingerprinted assets: must-revalidate (safe fallback).
    """

    def _is_fingerprinted(self, path: str) -> bool:
        return bool(_FINGERPRINT_RE.search(path or ""))

    async def get_response(self, path: str, scope) -> Response:
        resp = await super().get_response(path, scope)

        # Apply cache policy to both 200 (fresh) and 304 (conditional) responses.
        #
        # Setting Cache-Control on 304 is important for the transition period:
        # if a browser has an old cache entry (from a previous deploy that used
        # different headers), it will send a conditional GET and receive 304.
        # Without Cache-Control on the 304, the browser keeps its stale cache
        # semantics; with it, the browser updates the stored headers so the
        # next request uses the correct policy.
        if resp.status_code not in (200, 304):  # pragma: no cover — Starlette raises HTTPException for other codes
            return resp

        # Immutable caching for fingerprinted filenames.
        if self._is_fingerprinted(path):
            resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            # Non-fingerprinted assets: never cache. Using no-store (not just
            # no-cache) avoids the same-second mtime edge case where the server
            # returns 304 for a file that actually changed within the same second.
            # In production all assets are fingerprinted so this path is a fallback.
            resp.headers["Cache-Control"] = "no-store"
        return resp


class FallbackStaticFiles(CachingStaticFiles):
    """Static file serving with an optional fallback directory.

    Why this exists:
    - In local development we sometimes have a stale `static_dist/` directory.
      The app will mount it (because it exists) but it may not contain newly
      added images.
    - This wrapper keeps the production behaviour (prefer `static_dist/`) while
      ensuring missing files can still be served from `static/`.

    The fallback is only consulted when the primary directory returns 404.
    """

    def __init__(
        self,
        *,
        directory: str,
        fallback_directory: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(directory=directory, **kwargs)
        self._fallback: CachingStaticFiles | None = (
            CachingStaticFiles(directory=fallback_directory, **kwargs)
            if fallback_directory
            else None
        )

    async def get_response(self, path: str, scope) -> Response:
        try:
            resp = await super().get_response(path, scope)
        except HTTPException as exc:
            # Starlette may raise (instead of returning a Response) for 404.
            if exc.status_code == 404 and self._fallback is not None:
                return await self._fallback.get_response(path, scope)
            raise

        if resp.status_code == 404 and self._fallback is not None:
            return await self._fallback.get_response(path, scope)
        return resp

