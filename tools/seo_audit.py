#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from fnmatch import fnmatch

ROOT = Path(__file__).parent.parent


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str):
    text = text.lstrip("\ufeff")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def has_frontmatter_key(fm: str, key: str) -> bool:
    return re.search(rf"^{re.escape(key)}\s*:", fm, re.M) is not None


def word_count(body: str) -> int:
    body = re.sub(r"[`*_>#\[\]()-]", " ", body)
    words = re.findall(r"\b\w+\b", body)
    return len(words)


def link_matches(body: str, token: str) -> bool:
    return token in body


def load_thresholds(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_markdown():
    for p in ROOT.glob("content/**/*.md"):
        yield p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_thresholds(ROOT / args.config)
    min_word_count = cfg.get("min_word_count", {})
    required_links = cfg.get("required_links", [])
    require_faq = set(cfg.get("require_faq", []))
    include_globs = cfg.get("include_globs", [])
    exclude_globs = cfg.get("exclude_globs", [])

    failures = []

    for path in iter_markdown():
        rel = str(path.relative_to(ROOT))
        if include_globs and not any(fnmatch(rel, g) for g in include_globs):
            continue
        if exclude_globs and any(fnmatch(rel, g) for g in exclude_globs):
            continue
        text = read_file(path)
        fm, body = split_frontmatter(text)
        wc = word_count(body)

        target_wc = min_word_count.get(rel, min_word_count.get("default", 0))
        if wc < target_wc:
            failures.append(f"{rel}: word_count {wc} < {target_wc}")

        if rel in require_faq and not has_frontmatter_key(fm, "faq"):
            failures.append(f"{rel}: missing faq frontmatter")

        for rule in required_links:
            if fnmatch(rel, rule.get("glob", "")):
                for must in rule.get("must_include", []):
                    if not link_matches(body, must):
                        failures.append(f"{rel}: missing required link {must}")
                any_of = rule.get("at_least_one_of", [])
                if any_of and not any(link_matches(body, tok) for tok in any_of):
                    failures.append(f"{rel}: missing any of {any_of}")

    if failures:
        print("SEO audit failures:")
        for f in failures:
            print(f" - {f}")
        raise SystemExit(1)

    print("SEO audit passed.")


if __name__ == "__main__":
    main()
