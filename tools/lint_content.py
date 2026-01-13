import argparse
import re
import sys
from pathlib import Path

REQUIRED_BLOCKS = [
    "what the authority requires",
    "how we evaluate",
    "check in the engine",
    "disclaimer",
    "affiliate disclosure",
]

BANNED_WORDS = [
    "best",
    "recommend",
    "recommended",
    "guarantee",
    "guaranteed",
    "100%",
    "approved",
    "surely",
]

DEFAULT_SECTIONS = {"posts", "visas", "guides", "traps"}


def lint_text(text: str) -> list[str]:
    errors = []
    lower = text.lower()
    for block in REQUIRED_BLOCKS:
        if block not in lower:
            errors.append(f"missing block: {block}")
    if "snapshot=" not in lower:
        errors.append("missing snapshot= in deep link")
    for word in BANNED_WORDS:
        if re.search(rf"\b{re.escape(word)}\b", lower):
            errors.append(f"banned word: {word}")
    return errors


def lint_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    errors = lint_text(text)
    if errors:
        print(f"[ERROR] {path}")
        for err in errors:
            print("  ", err)
        return 1
    print(f"[OK] {path}")
    return 0


def should_lint(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    parts = {p.lower() for p in rel.parts}
    return bool(parts & DEFAULT_SECTIONS)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Single markdown file to lint")
    parser.add_argument("--root", type=str, default="content", help="Root content directory")
    args = parser.parse_args()

    if args.path:
        sys.exit(lint_file(Path(args.path)))

    root = Path(args.root)
    failures = 0
    for path in root.rglob("*.md"):
        if should_lint(path, root):
            failures += lint_file(path)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
