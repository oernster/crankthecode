from __future__ import annotations


from pathlib import Path
from zipfile import ZIP_STORED, ZipFile

from book.book_builder.pandoc_epub import _remove_nav_from_spine


def _make_minimal_epub(*, path: Path, opf_xml: str) -> None:
    """Create a minimal EPUB zip with a given OPF at `EPUB/content.opf`."""

    # EPUB spec: `mimetype` must be first entry and stored (no compression).
    with ZipFile(path, "w") as zf:
        zf.writestr(
            "mimetype",
            "application/epub+zip",
            compress_type=ZIP_STORED,
        )
        zf.writestr(
            "META-INF/container.xml",
            """<?xml version='1.0' encoding='UTF-8'?>
<container version='1.0' xmlns='urn:oasis:names:tc:opendocument:xmlns:container'>
  <rootfiles>
    <rootfile full-path='EPUB/content.opf' media-type='application/oebps-package+xml'/>
  </rootfiles>
</container>
""",
        )
        zf.writestr("EPUB/content.opf", opf_xml)
        # Keep `nav.xhtml` in the manifest, but it's fine if the file isn't used.
        zf.writestr("EPUB/nav.xhtml", "<html xmlns='http://www.w3.org/1999/xhtml'/>\n")


def test_remove_nav_from_spine_removes_nav_itemref_and_preserves_mimetype_rules(
    tmp_path: Path,
):
    epub = tmp_path / "test.epub"

    opf = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns='http://www.idpf.org/2007/opf' version='3.0'>
  <manifest>
    <item id='nav' href='nav.xhtml' media-type='application/xhtml+xml' properties='nav'/>
    <item id='ch001_xhtml' href='text/ch001.xhtml' media-type='application/xhtml+xml'/>
  </manifest>
  <spine>
    <itemref idref='nav'/>
    <itemref idref='ch001_xhtml'/>
  </spine>
</package>
"""
    _make_minimal_epub(path=epub, opf_xml=opf)

    _remove_nav_from_spine(epub_file=epub)

    with ZipFile(epub, "r") as zf:
        infos = zf.infolist()
        assert infos[0].filename == "mimetype"
        assert infos[0].compress_type == ZIP_STORED

        patched_opf = zf.read("EPUB/content.opf").decode("utf-8", errors="replace")
        assert "idref='nav'" not in patched_opf
        assert "idref=\"nav\"" not in patched_opf
        assert "ch001_xhtml" in patched_opf


def test_remove_nav_from_spine_is_noop_when_opf_missing(tmp_path: Path):
    epub = tmp_path / "missing_opf.epub"

    with ZipFile(epub, "w") as zf:
        zf.writestr(
            "mimetype",
            "application/epub+zip",
            compress_type=ZIP_STORED,
        )
        zf.writestr("META-INF/container.xml", "<container/>")

    # Should not raise.
    _remove_nav_from_spine(epub_file=epub)


def test_remove_nav_from_spine_is_noop_on_invalid_xml(tmp_path: Path):
    epub = tmp_path / "bad_xml.epub"
    _make_minimal_epub(path=epub, opf_xml="<not-xml")

    # Should not raise.
    _remove_nav_from_spine(epub_file=epub)

