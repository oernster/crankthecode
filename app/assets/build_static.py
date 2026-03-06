from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path


def _hash_bytes(data: bytes, *, length: int) -> str:
    return hashlib.sha256(data).hexdigest()[:length]


def _fingerprinted_name(filename: str, digest: str) -> str:
    p = Path(filename)
    suffix = p.suffix
    stem = p.name[: -len(suffix)] if suffix else p.name
    if suffix:
        return f"{stem}.{digest}{suffix}"
    return f"{stem}.{digest}"


def build_static_dist(
    *,
    static_src_dir: Path,
    static_dist_dir: Path,
    manifest_path: Path,
    hash_len: int = 10,
) -> dict[str, str]:
    """Build fingerprinted static assets into `static_dist_dir`.

    Output layout:
    - Copy each file to its original path (non-fingerprinted fallback).
    - Also emit a fingerprinted copy next to it.
    - Write `manifest.json` mapping `rel_path -> rel_fingerprinted_path`.
    """

    if not static_src_dir.exists():
        raise FileNotFoundError(f"static src dir not found: {static_src_dir}")

    if static_dist_dir.exists():
        shutil.rmtree(static_dist_dir)
    static_dist_dir.mkdir(parents=True, exist_ok=True)

    mapping: dict[str, str] = {}

    for src in sorted(static_src_dir.rglob("*")):
        if src.is_dir():
            continue

        rel = src.relative_to(static_src_dir).as_posix()
        if rel.endswith("/.gitkeep") or rel == ".gitkeep":
            continue

        data = src.read_bytes()
        digest = _hash_bytes(data, length=hash_len)

        # 1) Always copy the original path as a safe fallback.
        out_orig = static_dist_dir / rel
        out_orig.parent.mkdir(parents=True, exist_ok=True)
        out_orig.write_bytes(data)

        # 2) Emit the fingerprinted copy and record the manifest mapping.
        fp_name = _fingerprinted_name(src.name, digest)
        out_fp = out_orig.with_name(fp_name)
        out_fp.write_bytes(data)
        mapping[rel] = out_fp.relative_to(static_dist_dir).as_posix()

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(mapping, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description="Build fingerprinted /static assets")
    parser.add_argument(
        "--src",
        default=os.getenv("CTC_STATIC_SRC_DIR") or "static",
        help="Source static directory (default: static)",
    )
    parser.add_argument(
        "--dist",
        default=os.getenv("CTC_STATIC_DIST_DIR") or "static_dist",
        help="Output directory (default: static_dist)",
    )
    parser.add_argument(
        "--manifest",
        default=os.getenv("CTC_STATIC_MANIFEST_PATH") or "static_dist/manifest.json",
        help="Manifest JSON path (default: static_dist/manifest.json)",
    )
    parser.add_argument(
        "--hash-len",
        type=int,
        default=int(os.getenv("CTC_STATIC_HASH_LEN") or "10"),
        help="Hex chars to keep from sha256 (default: 10)",
    )
    args = parser.parse_args()

    build_static_dist(
        static_src_dir=Path(args.src),
        static_dist_dir=Path(args.dist),
        manifest_path=Path(args.manifest),
        hash_len=args.hash_len,
    )


if __name__ == "__main__":
    main()

