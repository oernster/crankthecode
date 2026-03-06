from __future__ import annotations

"""Tag parsing and normalization.

These utilities are used both by the web UI (filters/sidebars) and by the book
builder.
"""


def normalize_layer_slug(raw_slug: str) -> str:
    """Normalize a `layer:` slug into kebab-case."""

    raw = (raw_slug or "").strip().lower()
    if not raw:
        return ""

    if (
        raw.replace("-", "").isalnum()
        and "--" not in raw
        and not raw.startswith("-")
        and not raw.endswith("-")
    ):
        return raw

    out_chars: list[str] = []
    prev_dash = False
    for ch in raw:
        if ch.isalnum():
            out_chars.append(ch)
            prev_dash = False
            continue
        if ch in {" ", "_", "-"}:
            if not prev_dash and out_chars:
                out_chars.append("-")
                prev_dash = True
            continue

    return "".join(out_chars).strip("-")


def humanize_layer_slug(layer_slug: str) -> str:
    """Convert a normalized layer slug into a UI label."""

    cleaned = " ".join((layer_slug or "").strip().replace("_", "-").split("-"))
    cleaned = " ".join(cleaned.split())
    if not cleaned:
        return ""

    label = cleaned.title()
    acronym_map = {
        "Cto": "CTO",
    }
    return " ".join(acronym_map.get(p, p) for p in label.split(" "))


def extract_layer_slugs_from_tags(tags: list[str]) -> set[str]:
    """Extract normalized `layer:` slugs from a post's tag list."""

    out: set[str] = set()
    for t in tags or []:
        raw = (t or "").strip()
        if not raw:
            continue
        if not raw.lower().startswith("layer:"):
            continue
        tail = raw.split(":", 1)[1].strip()
        slug = normalize_layer_slug(tail)
        if slug:
            out.add(slug)
    return out


def primary_layer_slug_from_tags(tags: list[str]) -> str | None:
    """Return the first `layer:` slug in the original tag order (if any)."""

    for t in tags or []:
        raw = (t or "").strip()
        if not raw.lower().startswith("layer:"):
            continue
        tail = raw.split(":", 1)[1].strip()
        slug = normalize_layer_slug(tail)
        if slug:
            return slug
    return None
