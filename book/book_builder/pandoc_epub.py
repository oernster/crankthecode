from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

import xml.etree.ElementTree as ET


def is_output_up_to_date(*, output_file: Path, source_files: Sequence[Path]) -> bool:
    if not output_file.exists():
        return False

    output_time = output_file.stat().st_mtime
    latest_source_time = max(
        (p.stat().st_mtime for p in source_files if p.exists()),
        default=0,
    )
    return output_time >= latest_source_time


@dataclass(frozen=True, slots=True)
class PandocEpubBuilder:
    metadata_file: Path
    combined_markdown_file: Path
    css_file: Path
    cover_file: Path
    output_file: Path

    def build(self) -> bool:
        sources = [
            self.combined_markdown_file,
            self.metadata_file,
            self.css_file,
            self.cover_file,
        ]
        if is_output_up_to_date(output_file=self.output_file, source_files=sources):
            print("EPUB already up to date — skipping build.")
            return False

        cmd: list[str] = [
            "pandoc",
            str(self.metadata_file),
            str(self.combined_markdown_file),
            "--css",
            str(self.css_file),
            "--split-level=2",
            "--toc",
            "--toc-depth=3",
            "--number-sections",
            "--top-level-division=part",
            "--epub-cover-image",
            str(self.cover_file),
            "--metadata",
            "pagetitle=Decision Architecture",
            "--embed-resources",
            "-o",
            str(self.output_file),
        ]

        subprocess.run(cmd, check=True)

        # Post-process the EPUB for KDP print preview.
        # KDP strips certain EPUB-only navigation markup (e.g. <nav epub:type="toc">)
        # as "non-printable" but still paginates it if it's in the spine.
        # That produces large blank page ranges.
        _remove_nav_from_spine(epub_file=self.output_file)
        return True


_OPF_NS = {
    "opf": "http://www.idpf.org/2007/opf",
}


def _remove_nav_from_spine(*, epub_file: Path) -> None:
    """Remove the `nav` itemref from the OPF spine.

    Pandoc emits `nav.xhtml` and includes it in the OPF spine. KDP's print
    conversion strips the nav markup and can render it as blank pages.

    We keep the nav document for EPUB readers (it's still in the manifest with
    `properties="nav"`), but remove it from the reading order by deleting its
    <itemref> from the OPF spine.
    """

    if not epub_file.exists():
        return

    with ZipFile(epub_file, "r") as zf:
        try:
            opf_bytes = zf.read("EPUB/content.opf")
        except KeyError:
            return

    try:
        root = ET.fromstring(opf_bytes)
    except ET.ParseError:
        return

    spine = root.find("opf:spine", _OPF_NS)
    if spine is None:
        return

    itemrefs = spine.findall("opf:itemref", _OPF_NS)
    to_remove = [ir for ir in itemrefs if ir.attrib.get("idref") == "nav"]
    if not to_remove:
        return

    for ir in to_remove:
        spine.remove(ir)
    changed = True

    if not changed:
        return

    patched_opf = ET.tostring(root, encoding="utf-8", xml_declaration=True)

    tmp_file = epub_file.with_suffix(epub_file.suffix + ".tmp")
    with ZipFile(epub_file, "r") as src, ZipFile(tmp_file, "w") as dst:
        # EPUB spec: `mimetype` must be first and stored (no compression)
        names = src.namelist()
        if "mimetype" in names:
            dst.writestr(
                "mimetype",
                src.read("mimetype"),
                compress_type=ZIP_STORED,
            )

        for info in src.infolist():
            if info.filename == "mimetype":
                continue

            data = patched_opf if info.filename == "EPUB/content.opf" else src.read(info.filename)

            # Use deflate for everything else.
            dst.writestr(info.filename, data, compress_type=ZIP_DEFLATED)

    tmp_file.replace(epub_file)
