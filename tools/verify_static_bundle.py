import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("VERIFY_ROOT", Path(__file__).parent.parent))


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        fail(f"Missing {label}: {path}")
    if path.stat().st_size == 0:
        fail(f"Empty {label}: {path}")


def main() -> None:
    ui = ROOT / "static" / "ui" / "index.html"
    index = ROOT / "static" / "data" / "ui_index.json"
    sources_dir = ROOT / "static" / "sources"

    require_file(ui, "ui index")
    require_file(index, "ui index json")

    if not sources_dir.exists():
        fail("Missing static/sources directory")

    sources = [p for p in sources_dir.rglob("*") if p.is_file()]
    if not sources:
        fail("No source files found in static/sources")

    print("Static bundle verification passed")


if __name__ == "__main__":
    main()
