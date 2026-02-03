#!/usr/bin/env python3
import re
from pathlib import Path


def extract_evidence_section(text: str) -> str | None:
    pattern = re.compile(
        r"^##\s+Evidence\s+log.*?$\n(?P<body>.*?)(?=^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return None
    return match.group("body")


def preview_lines(section: str, limit: int = 2) -> list[str]:
    lines = [line.strip() for line in section.strip().splitlines() if line.strip()]
    return lines[:limit]


def main() -> None:
    content_root = Path("content")
    matches: list[tuple[str, list[str]]] = []

    for path in sorted(content_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        section = extract_evidence_section(text)
        if not section:
            continue
        if "Source: UNKNOWN" in section:
            rel = str(path)
            preview = preview_lines(section)
            matches.append((rel, preview))

    lines: list[str] = []
    lines.append(f"Total: {len(matches)}")
    for rel, preview in matches:
        lines.append(rel)
        for pline in preview:
            lines.append(f"  {pline}")

    output = "\n".join(lines) + "\n"
    print(output, end="")

    report_path = Path("docs/reports/evidence-unknown-files.txt")
    report_path.write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
