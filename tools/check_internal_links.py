#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONTENT = ROOT / "content"


def resolve_internal_target(target: str) -> bool:
    target = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not target:
        return True
    if target.startswith("/ui/") or target == "/ui":
        return (ROOT / "ui" / "index.html").exists()

    # Evidence files are served as static assets (sources/ -> static/sources/).
    # They are real downloadable links, not content pages, so resolve them
    # against the source-of-truth sources/ directory.
    if target.startswith("/sources/"):
        return (ROOT / target.strip("/")).exists()

    target_path = target.strip("/")
    candidates = [
        CONTENT / f"{target_path}.md",
        CONTENT / target_path / "index.md",
        CONTENT / target_path / "_index.md",
    ]
    return any(c.exists() for c in candidates)


def main() -> int:
    pattern = re.compile(r"\[[^\]]+\]\((/[^)]+)\)")
    failures = []
    for md in CONTENT.rglob("*.md"):
        rel = md.relative_to(ROOT).as_posix()
        text = md.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            href = match.group(1).strip()
            if not resolve_internal_target(href):
                failures.append(f"{rel}: broken internal link {href}")

    if failures:
        print("Internal link check failures:")
        for item in failures:
            print(f" - {item}")
        return 1

    print("Internal link integrity check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
