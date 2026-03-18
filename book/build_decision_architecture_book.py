"""Build the Decision Architecture book (EPUB).

This file is kept as a thin script entrypoint. Implementation lives under
[`book.book_builder`](book/book_builder/__init__.py:1).
"""

from __future__ import annotations

import sys
from pathlib import Path


def _find_repo_root_for_script(*, start: Path) -> Path:
    """Find the repository root when this script is executed as a file.

    When running `python book/build_decision_architecture_book.py` *from inside the
    `book/` directory*, Python's import root becomes `book/`, meaning `import book`
    fails (because the repo root isn't on `sys.path`).

    We locate the repo root by walking parents until we find `pyproject.toml`, then
    insert that directory into `sys.path`.
    """

    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise RuntimeError(f"Unable to locate repo root from: {start}")


_REPO_ROOT = _find_repo_root_for_script(start=Path(__file__))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


from book.book_builder.orchestrator import BuildOrchestrator  # noqa: E402
from book.book_builder.paths import BookPaths, find_repo_root  # noqa: E402

SECTION_PRIORITY = {
    "architecture": 1,
    "cto-operating-model": 2,
    "decision-systems": 3,
    "organisational-structure": 4,
    "structural-design": 5,
}


# This book is the essay collection. Explicitly exclude DA Patterns posts.
_EXCLUDED_CATEGORY = "cat:decision-architecture-patterns"


def main() -> None:
    repo_root = find_repo_root(start=Path(__file__).resolve())
    paths = BookPaths.from_repo_root(repo_root)
    BuildOrchestrator(
        paths=paths,
        section_priority=SECTION_PRIORITY,
        required_category=f"!{_EXCLUDED_CATEGORY}",
    ).build()


if __name__ == "__main__":
    main()
