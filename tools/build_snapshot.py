import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
SNAPSHOTS = Path(os.environ.get("SNAPSHOT_ROOT", DATA / "snapshots"))

VISAS = DATA / "visas"
PRODUCTS = DATA / "products"
MAPPINGS = DATA / "mappings"
UI_INDEX = DATA / "ui_index.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def resolve_snapshot_id() -> str:
    env_id = os.environ.get("SNAPSHOT_ID")
    if env_id:
        return env_id
    if UI_INDEX.exists():
        try:
            data = json.loads(UI_INDEX.read_text(encoding="utf-8"))
            if data.get("snapshot_id"):
                return str(data["snapshot_id"])
        except Exception:
            pass
    return datetime.utcnow().date().isoformat()


def build_manifest(snapshot_dir: Path, snapshot_id: str) -> None:
    files = []
    for path in sorted(snapshot_dir.rglob("*")):
        if path.is_dir():
            continue
        rel = path.relative_to(snapshot_dir).as_posix()
        files.append(
            {
                "path": rel,
                "sha256": sha256(path),
                "size": path.stat().st_size,
            }
        )
    manifest = {
        "snapshot_id": snapshot_id,
        "built_at": datetime.utcnow().isoformat() + "Z",
        "files": files,
    }
    (snapshot_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )


def main() -> None:
    snapshot_id = resolve_snapshot_id()
    snapshot_dir = SNAPSHOTS / snapshot_id
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    copy_tree(VISAS, snapshot_dir / "visas")
    copy_tree(PRODUCTS, snapshot_dir / "products")
    copy_tree(MAPPINGS, snapshot_dir / "mappings")

    if not UI_INDEX.exists():
        raise FileNotFoundError(f"Missing {UI_INDEX}")
    copy_file(UI_INDEX, snapshot_dir / "ui_index.json")

    build_manifest(snapshot_dir, snapshot_id)
    print(f"Snapshot written to {snapshot_dir}")


if __name__ == "__main__":
    main()
