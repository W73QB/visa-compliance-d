#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def word_count(body: str) -> int:
    body = re.sub(r"[`*_>#\[\]()-]", " ", body)
    words = re.findall(r"\b\w+\b", body)
    return len(words)


def split_frontmatter(text: str):
    text = text.lstrip("\ufeff")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def main():
    targets_path = ROOT / "tools" / "editorial_targets.json"
    targets = json.loads(targets_path.read_text(encoding="utf-8"))

    failures = []

    for rel_path, (min_wc, max_wc) in targets.items():
        file_path = ROOT / rel_path

        if not file_path.exists():
            failures.append(f"{rel_path}: file not found")
            continue

        text = file_path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        wc = word_count(body)

        if wc < min_wc:
            failures.append(f"{rel_path}: {wc} words < {min_wc} minimum")
        elif wc > max_wc:
            failures.append(f"{rel_path}: {wc} words > {max_wc} maximum")

    if failures:
        print("Editorial target violations:")
        for f in failures:
            print(f" - {f}")
        sys.exit(1)

    print("All files within editorial targets.")


if __name__ == "__main__":
    main()
