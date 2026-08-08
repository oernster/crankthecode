from __future__ import annotations

from typing import Protocol


class AssetUrls(Protocol):
    """Port for resolving static asset URLs to their fingerprinted equivalents.

    The use cases need to rewrite `/static/...` references without knowing how
    fingerprinting is configured, where the manifest lives or whether one is in
    use at all. The manifest-backed implementation satisfies this structurally;
    a test can supply an empty manifest and get identity behaviour.
    """

    def resolve_url_or_path(self, url_or_path: str) -> str:
        """Return the fingerprinted equivalent of a URL or path.

        Absolute URLs and anything outside `/static/` are returned unchanged.
        """

    def rewrite_html_static_urls(self, html: str) -> str:
        """Rewrite every `/static/...` reference inside rendered HTML."""
