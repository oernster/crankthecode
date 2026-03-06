import re
import subprocess
from pathlib import Path
import yaml

SOURCE_DIR = Path(r"C:\Users\Oliver\Development\crankthecode\posts")

OUTPUT_FILE = SOURCE_DIR / "Decision-Architecture.epub"
TEMP_COMBINED = SOURCE_DIR / "_combined_book.md"

CSS_FILE = SOURCE_DIR / "_book_style.css"
METADATA_FILE = SOURCE_DIR / "_metadata.yaml"
COVER_FILE = SOURCE_DIR / "_cover.png"

LAYER_TO_SECTION = {
    "architecture": "Architecture",
    "cto-operating-model": "CTO Operating Model",
    "decision-systems": "Decision Systems",
    "organisational-structure": "Organisational Structure",
    "structural-design": "Structural Design",
}

SECTION_ORDER = [
    "Architecture",
    "CTO Operating Model",
    "Decision Systems",
    "Organisational Structure",
    "Structural Design",
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
HEADING_NUMBER_PREFIX_RE = re.compile(r"^(\d+(?:\.\d+)*)(?:[.)])?\s+")


def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    meta = yaml.safe_load(match.group(1))
    body = text[match.end():]
    return meta or {}, body


def extract_layer(tags):
    for tag in tags:
        if isinstance(tag, str) and tag.startswith("layer:"):
            return tag.split(":", 1)[1].strip()
    return None


def strip_number(text: str) -> str:
    return HEADING_NUMBER_PREFIX_RE.sub("", text).strip()


def normalize_content(content: str, chapter_number: int) -> str:
    lines = content.replace("\r\n", "\n").split("\n")

    if lines and lines[0].startswith("# "):
        lines.pop(0)

    result = []
    h2_count = 0

    for line in lines:
        if line.startswith("# "):
            line = "#" + line

        m = re.match(r"^(#{2,6})\s+(.*)", line)
        if m:
            hashes, text = m.groups()
            text = strip_number(text)

            if hashes == "##":
                h2_count += 1
                text = f"{chapter_number}.{h2_count} {text}"

            line = f"{hashes} {text}"

        result.append(line)

    return "\n".join(result)


def collect_files():
    return [f for f in SOURCE_DIR.glob("*.md") if not f.name.startswith("_")]


def build_markdown():
    files = collect_files()

    about = None
    crystal = None
    sections = {s: [] for s in SECTION_ORDER}

    for f in files:
        text = f.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        if f.name == "about-me.md":
            about = (meta, body, f.name)
            continue

        if f.name == "crystal.md":
            crystal = (meta, body, f.name)
            continue

        tags = meta.get("tags", [])
        layer = extract_layer(tags)

        if layer:
            section = LAYER_TO_SECTION.get(layer)
            if section:
                sections[section].append((meta, body, f.name))

    for section_name in sections:
        sections[section_name].sort(key=lambda x: x[2])

    toc = ["## Contents", ""]
    body_blocks = []

    chapter = 0
    part = 1

    if about:
        _, body, _ = about
        chapter += 1
        title = "Introduction"
        body = normalize_content(body, chapter)

        toc.append(f"- {chapter}. {title}")
        for line in body.split("\n"):
            if line.startswith("## "):
                toc.append(f"  - {line[3:].strip()}")
        toc.append("")

        body_blocks.append(f"# {title}\n\n{body}\n\n")

    if crystal:
        meta, body, _ = crystal
        chapter += 1
        title = meta.get("title", "Crystalline")
        body = normalize_content(body, chapter)

        toc.append(f"- {chapter}. {title}")
        for line in body.split("\n"):
            if line.startswith("## "):
                toc.append(f"  - {line[3:].strip()}")
        toc.append("")

        body_blocks.append(f"# {title}\n\n{body}\n\n")

    for section in SECTION_ORDER:
        entries = sections.get(section, [])
        if not entries:
            continue

        part_title = f"Part {part} - {section}"
        toc.append(f"- {part_title}")

        body_blocks.append(f"# {part_title}\n\n")

        for meta, body, filename in entries:
            chapter += 1
            title = meta.get("title", Path(filename).stem)
            body = normalize_content(body, chapter)

            toc.append(f"  - {chapter}. {title}")
            for line in body.split("\n"):
                if line.startswith("## "):
                    toc.append(f"    - {line[3:].strip()}")
            toc.append("")

            body_blocks.append(f"## {chapter}. {title}\n\n{body}\n\n")

        part += 1

    with open(TEMP_COMBINED, "w", encoding="utf-8") as f:
        f.write("\n".join(toc).rstrip())
        f.write("\n\n")
        for block in body_blocks:
            f.write(block)


def build_epub():
    cmd = [
        "pandoc",
        str(METADATA_FILE),
        str(TEMP_COMBINED),
        "--css", str(CSS_FILE),
        "--split-level=1",
        "--epub-cover-image", str(COVER_FILE),
        "-o", str(OUTPUT_FILE),
    ]
    subprocess.run(cmd, check=True)


def main():
    build_markdown()
    build_epub()

    if TEMP_COMBINED.exists():
        TEMP_COMBINED.unlink()

    print("Book created successfully")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()