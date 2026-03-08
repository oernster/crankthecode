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

        # Only apply policy to successful static responses.
        if resp.status_code != 200:
            return resp

        # Immutable caching for fingerprinted filenames.
        if self._is_fingerprinted(path):
            resp.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        else:
            # Safe fallback: browsers/CDNs can cache but must revalidate.
            resp.headers["Cache-Control"] = "no-cache, must-revalidate"
        return resp


class FallbackStaticFiles(CachingStaticFiles):
    """Static file serving with an optional fallback directory.

    Why this exists:
    - In local development we sometimes have a stale `static_dist/` directory.
      The app will mount it (because it exists), but it may not contain newly
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

