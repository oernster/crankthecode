from __future__ import annotations

import re


def normalize_whitespace(text: str) -> str:
    """Collapse whitespace into single spaces and strip.

    Also replaces NBSP with regular spaces.
    """

    out = (text or "").replace("\u00a0", " ")
    out = re.sub(r"\s+", " ", out)
    return out.strip()


def _strip_leading_blank_lines(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    return lines


def _remove_leading_heading(lines: list[str], heading_text: str) -> list[str]:
    lines = _strip_leading_blank_lines(lines)
    if not lines:
        return lines

    match = re.match(r"^(#{1,6})\s+(.*)$", lines[0])
    if not match:
        return lines

    existing = normalize_whitespace(match.group(2)).lower()
    target = normalize_whitespace(heading_text).lower()

    if existing == target:
        lines.pop(0)
        lines = _strip_leading_blank_lines(lines)
    return lines


def normalize_content(content: str, *, remove_heading_text: str | None = None) -> str:
    """Normalize markdown content for inclusion inside the book.

    Rules (kept intentionally compatible with the original script):
    - normalize newlines
    - strip leading blank lines
    - drop a leading H1 (common in individual posts)
    - optionally drop a specific leading heading
    - rebase headings so the smallest heading becomes ###
    - cap at H6 and prevent skipped levels
    """

    lines = (content or "").replace("\r\n", "\n").split("\n")
    lines = _strip_leading_blank_lines(lines)

    if lines and re.match(r"^#\s+", lines[0]):
        lines.pop(0)

    if remove_heading_text:
        lines = _remove_leading_heading(lines, remove_heading_text)

    min_level: int | None = None
    for line in lines:
        match = re.match(r"^(#{1,6})\s+", line)
        if not match:
            continue
        level = len(match.group(1))
        if min_level is None or level < min_level:
            min_level = level

    if min_level is None:
        return "\n".join(lines)

    result: list[str] = []
    last_level: int | None = None
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.*)", line)
        if match:
            hashes, heading = match.groups()
            level = len(hashes)

            new_level = level - min_level + 3
            new_level = min(new_level, 6)

            if last_level is not None and new_level > last_level + 1:
                new_level = last_level + 1

            last_level = new_level
            line = f"{'#' * new_level} {normalize_whitespace(heading)}"

        result.append(line)

    return "\n".join(result)
