from __future__ import annotations

import re
from typing import Optional

from fastapi.staticfiles import StaticFiles
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

