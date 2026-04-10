from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


_FINGERPRINT_RE = re.compile(r"\.[0-9a-f]{8,}\.")


_ASSET_DEBUG_ENV = "CTC_ASSET_MANIFEST_DEBUG"
_ASSET_FORCE_LOAD_ENV = "CTC_FORCE_STATIC_DIST_MANIFEST"


def _truthy_env(name: str) -> bool:
    return (os.getenv(name) or "").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }


def _use_static_dist() -> bool:
    """Return True when the app should use fingerprinted `static_dist/` assets.

    Local dev should default to `static/` to avoid stale build output breaking
    images. Production explicitly opts into `static_dist/`.
    """

    return _truthy_env("CTC_USE_STATIC_DIST")


def _debug_enabled() -> bool:
    """Enable one-shot runtime diagnostics for asset manifest resolution.

    Note: `get_asset_manifest()` is cached (single evaluation per process), so
    logging here is low-noise even when enabled.
    """

    return _truthy_env(_ASSET_DEBUG_ENV)


def _normalize_rel_path(path: str) -> str:
    # Manifest keys always use forward slashes and no leading slash.
    p = (path or "").strip().lstrip("/")
    return p.replace("\\", "/")


@dataclass(frozen=True, slots=True)
class AssetManifest:
    """Mapping from logical static paths to fingerprinted filenames."""

    mapping: dict[str, str]

    @classmethod
    def load(cls, manifest_path: Path) -> "AssetManifest":
        try:
            raw = manifest_path.read_text(encoding="utf-8")
        except OSError:
            return cls(mapping={})

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return cls(mapping={})

        if not isinstance(data, dict):
            return cls(mapping={})

        mapping: dict[str, str] = {}
        for k, v in data.items():
            if not isinstance(k, str) or not isinstance(v, str):
                continue
            mapping[_normalize_rel_path(k)] = _normalize_rel_path(v)
        return cls(mapping=mapping)

    def resolve_rel(self, rel_path: str) -> str:
        rel = _normalize_rel_path(rel_path)
        return self.mapping.get(rel, rel)

    def static_url(self, rel_path: str) -> str:
        """Return a URL path under `/static/...` for a source-relative path."""

        rel = self.resolve_rel(rel_path)
        return f"/static/{rel}".replace("//", "/")

    def resolve_url_or_path(self, url_or_path: str) -> str:
        """Resolve an existing URL/path to its fingerprinted equivalent.

        - Absolute URLs are returned unchanged.
        - `/static/<rel>` paths are rewritten to `/static/<fingerprinted>` when known.
        - Any other value is returned unchanged.
        """

        raw = (url_or_path or "").strip()
        if not raw:
            return raw
        lower = raw.lower()
        if lower.startswith("http://") or lower.startswith("https://"):
            return raw
        if raw.startswith("/static/"):
            rel = raw[len("/static/") :]
            return self.static_url(rel)
        return raw

    def rewrite_html_static_urls(self, html: str) -> str:
        """Rewrite `/static/...` URLs inside rendered HTML.

        We target the most common places assets occur:
        - `src="/static/..."`
        - `href="/static/..."`
        - CSS `url(/static/...)` inside inline styles
        """

        if not html:
            return html

        # src/href attributes
        attr_re = re.compile(
            r"(?P<prefix>\b(?:src|href)=['\"])(?P<url>/static/(?P<rel>[^'\"?#]+))",
            flags=re.IGNORECASE,
        )

        def _attr_sub(m: re.Match[str]) -> str:
            rel = m.group("rel")
            return f"{m.group('prefix')}{self.static_url(rel)}"

        out = attr_re.sub(_attr_sub, html)

        # CSS url(...) patterns (very conservative)
        css_url_re = re.compile(
            r"(?P<prefix>url\(['\"]?)(?P<url>/static/(?P<rel>[^'\")?#]+))",
            flags=re.IGNORECASE,
        )

        def _css_sub(m: re.Match[str]) -> str:
            rel = m.group("rel")
            return f"{m.group('prefix')}{self.static_url(rel)}"

        return css_url_re.sub(_css_sub, out)

    @staticmethod
    def is_fingerprinted_path(path: str) -> bool:
        return bool(_FINGERPRINT_RE.search(path or ""))


def _default_manifest_path() -> Path:
    return Path(os.getenv("CTC_STATIC_MANIFEST_PATH") or "static_dist/manifest.json")


@lru_cache(maxsize=1)
def get_asset_manifest() -> AssetManifest:
    debug = _debug_enabled()
    raw_flag = os.getenv("CTC_USE_STATIC_DIST")
    use_dist = _use_static_dist()
    force_load = _truthy_env(_ASSET_FORCE_LOAD_ENV)
    manifest_path = _default_manifest_path()

    # Always print this single line once per process (function is cached).
    # It directly answers: "Is the env flag applied at runtime?"
    print(f"USE_STATIC_DIST: {use_dist} (raw={raw_flag!r})")

    if debug:
        # These logs are intentionally explicit and copy/paste friendly.
        print(
            "ASSET_MANIFEST_DEBUG:",
            {
                "CTC_USE_STATIC_DIST": raw_flag,
                "CTC_STATIC_MANIFEST_PATH": os.getenv("CTC_STATIC_MANIFEST_PATH"),
                "CTC_FORCE_STATIC_DIST_MANIFEST": os.getenv(_ASSET_FORCE_LOAD_ENV),
                "computed_use_static_dist": use_dist,
                "computed_force_load": force_load,
                "manifest_path": str(manifest_path),
                "manifest_exists": manifest_path.exists(),
                "cwd": str(Path.cwd()),
            },
        )

    # If we're not serving from `static_dist/`, do not rewrite URLs to
    # fingerprinted filenames (they won't exist under the mounted `/static`).
    #
    # `CTC_FORCE_STATIC_DIST_MANIFEST=1` is a temporary diagnostic escape hatch
    # to prove that the manifest+templates wiring works even when the env flag
    # is not applied correctly in production.
    if not use_dist and not force_load:
        if debug:
            print(
                "ASSET_MANIFEST_DEBUG: manifest rewriting disabled (set "
                f"{_ASSET_FORCE_LOAD_ENV}=1 to force-load manifest for testing)"
            )
        return AssetManifest(mapping={})

    manifest = AssetManifest.load(manifest_path)
    if debug:
        print("MANIFEST KEYS:", list(manifest.mapping.keys())[:20])
        print("ASSET_MANIFEST_DEBUG: manifest_key_count=", len(manifest.mapping))
    return manifest


def reset_asset_manifest_cache() -> None:
    """Clear the in-process manifest cache.

    Useful in tests or development when the build step regenerates the manifest.
    """

    get_asset_manifest.cache_clear()


def asset_url(rel_path: str) -> str:
    """Template-friendly helper for `/static/` URLs."""

    return get_asset_manifest().static_url(rel_path)

