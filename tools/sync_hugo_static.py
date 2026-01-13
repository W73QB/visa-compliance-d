import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> None:
    static = ROOT / "static"
    static.mkdir(exist_ok=True)

    ui_src = ROOT / "ui"
    if ui_src.exists():
        copy_tree(ui_src, static / "ui")

    index_src = ROOT / "data" / "ui_index.json"
    if index_src.exists():
        copy_file(index_src, static / "data" / "ui_index.json")

    sources_src = ROOT / "sources"
    if sources_src.exists():
        copy_tree(sources_src, static / "sources")

    snapshots_src = ROOT / "data" / "snapshots"
    if snapshots_src.exists():
        copy_tree(snapshots_src, static / "snapshots")

    print("Synced UI/data/sources into static/ for Hugo")


if __name__ == "__main__":
    main()
