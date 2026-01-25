import os
import shutil
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SYNC_ROOT", Path(__file__).parent.parent))


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    static = ROOT / "static"
    static.mkdir(exist_ok=True)

    ui_src = ROOT / "ui"
    if not ui_src.exists():
        fail("Missing ui/ directory")
    css_src = ui_src / "style.css"
    if not css_src.exists():
        fail("Missing ui/style.css. Run npm run build:css before sync.")
    copy_tree(ui_src, static / "ui")

    index_src = ROOT / "data" / "ui_index.json"
    if not index_src.exists():
        fail("Missing data/ui_index.json")
    copy_file(index_src, static / "data" / "ui_index.json")

    sources_src = ROOT / "sources"
    release = os.environ.get("RELEASE_BUILD", "").lower() in {"1", "true", "yes"}
    if sources_src.exists():
        copy_tree(sources_src, static / "sources")
    elif release:
        fail("Missing sources/ directory in release mode")

    snapshots_src = ROOT / "data" / "snapshots"
    if snapshots_src.exists():
        copy_tree(snapshots_src, static / "snapshots")

    headers_src = ROOT / "ops" / "headers" / "_headers"
    if headers_src.exists():
        copy_file(headers_src, static / "_headers")

    print("Synced UI/data/sources into static/ for Hugo")


if __name__ == "__main__":
    main()
