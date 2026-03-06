from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


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
        return True
