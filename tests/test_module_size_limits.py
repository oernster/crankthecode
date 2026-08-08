"""The 400-line module cap, measured rather than remembered.

Nothing in this repository reported file size before this test existed, so four
files sat over the cap unnoticed. Both halves of the rule are asserted
separately, one test each, so a red run names which half was broken.

Scope is Python by decision rather than by omission. `static/search.js` sits
outside it and stays there: see the "Not debt" section of TECH_DEBT.md, which
records why splitting a browser IIFE would break the fingerprinted build. Do not
widen this scan to JavaScript without reading that entry first.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# REFACTORING RULE (the 5% rule): 400 is the limit and the normal target, so a
# file below it and clear of the band below needs nothing doing to it.
#
# 5% of 400 is 20, so >380 and <400 (381 to 399) is the danger band. A file in
# that band is reduced to <=350, never left at 399. That covers both a file that
# grew into the band and one refactored down from over the cap, which must land
# at <=350 rather than stopping the moment it clears 400.
#
# Shaving a line or two to sit just under the cap buys nothing: the next edit
# breaks it again and the same file gets refactored repeatedly. Extract a
# cohesive concern instead.
_CAP_LINES = 400

# 5% of the cap, derived rather than written as 380, so the two numbers cannot
# drift apart if the cap ever moves.
_DANGER_BAND_PERCENT = 5
_DANGER_BAND_START = _CAP_LINES - (_CAP_LINES * _DANGER_BAND_PERCENT) // 100

# Where a file in the band has to land. Not merely under the cap: see above.
_LANDING_LINES = 350

# Build and packaging scripts are exempt. They are linear recipes read top to
# bottom, where splitting a sequence of steps across modules costs more than it
# buys. Listed rather than left to chance.
_BUILD_SCRIPTS = frozenset({"generate_scripts.py", "stamp_version.py"})

_EXCLUDED_DIRS = frozenset(
    {".git", "__pycache__", "venv", ".venv", "static_dist", ".pytest_cache"}
)

_SCANNED_ROOTS = ("app", "tests")


@dataclass(frozen=True, slots=True)
class SizedFile:
    path: str
    lines: int


def _repo_root() -> Path:
    # tests/test_module_size_limits.py -> tests -> repo root
    return Path(__file__).resolve().parents[1]


def _count_physical_lines(path: Path) -> int:
    # Physical lines, not logical LOC. Tolerant decoding so an odd encoding
    # cannot make a file silently escape the rule.
    return sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore"))


def _in_scope_files(root: Path) -> list[SizedFile]:
    found: list[SizedFile] = []

    candidates = [p for name in _SCANNED_ROOTS for p in (root / name).rglob("*.py")]
    candidates += [p for p in root.glob("*.py")]

    for path in candidates:
        if set(path.parts) & _EXCLUDED_DIRS:
            continue
        if path.name in _BUILD_SCRIPTS:
            continue
        found.append(
            SizedFile(
                path=path.relative_to(root).as_posix(),
                lines=_count_physical_lines(path),
            )
        )

    return found


def _report(offenders: list[SizedFile]) -> str:
    ordered = sorted(offenders, key=lambda f: (f.lines, f.path), reverse=True)
    return "\n".join(f"- {f.lines:4d}  {f.path}" for f in ordered)


def test_no_python_module_exceeds_the_cap() -> None:
    offenders = [f for f in _in_scope_files(_repo_root()) if f.lines > _CAP_LINES]

    if offenders:
        raise AssertionError(
            f"Every in-scope *.py must be <= {_CAP_LINES} lines. Extract a "
            f"cohesive concern and land the result at <= {_LANDING_LINES}, not "
            "just under the cap.\n" + _report(offenders)
        )


def test_no_python_module_sits_in_the_danger_band() -> None:
    """The 5% rule, enforced rather than only documented.

    A file at 399 passes the cap and then fails on the next edit made to it, for
    a reason unrelated to that edit. Catching it here deals with it while it is
    still cheap, which is the whole point of the band.
    """

    offenders = [
        f
        for f in _in_scope_files(_repo_root())
        if _DANGER_BAND_START < f.lines < _CAP_LINES
    ]

    if offenders:
        raise AssertionError(
            f"The danger band ({_DANGER_BAND_START + 1} to {_CAP_LINES - 1} "
            f"lines) is occupied. Take each file to <= {_LANDING_LINES} by "
            "extracting a cohesive concern; do not shave lines to sit just "
            "under the cap, because the next edit undoes it.\n" + _report(offenders)
        )


def test_the_size_scan_reaches_both_the_application_and_the_tests() -> None:
    """The cap is only as good as the surface it is measured over."""

    scanned = {f.path for f in _in_scope_files(_repo_root())}

    assert any(p.startswith("app/") for p in scanned)
    assert any(p.startswith("tests/") for p in scanned)
    assert "main.py" in scanned
