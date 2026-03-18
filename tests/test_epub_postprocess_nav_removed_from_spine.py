from __future__ import annotations


from pathlib import Path
from zipfile import ZipFile


def _spine_itemrefs(opf_xml: str) -> list[str]:
    # Very small, dependency-free parse: good enough for this test.
    # Pandoc may prefix namespaces, so we match on "itemref" regardless.
    out: list[str] = []
    for line in opf_xml.splitlines():
        if "itemref" not in line:
            continue
        if "idref=" not in line:
            continue
        # Extract idref="..."
        start = line.find('idref="')
        if start == -1:
            continue
        start += len('idref="')
        end = line.find('"', start)
        if end == -1:
            continue
        out.append(line[start:end])
    return out


def test_decision_architecture_epub_spine_does_not_include_nav():
    epub = Path("docs") / "Decision-Architecture.epub"
    assert epub.exists(), "Build the EPUB before running this test"

    with ZipFile(epub, "r") as zf:
        opf = zf.read("EPUB/content.opf").decode("utf-8", errors="replace")

    spine = _spine_itemrefs(opf)
    assert "nav" not in spine


def test_patterns_epub_spine_does_not_include_nav():
    epub = Path("docs") / "decision-architecture-patterns.epub"
    assert epub.exists(), "Build the EPUB before running this test"

    with ZipFile(epub, "r") as zf:
        opf = zf.read("EPUB/content.opf").decode("utf-8", errors="replace")

    spine = _spine_itemrefs(opf)
    assert "nav" not in spine

