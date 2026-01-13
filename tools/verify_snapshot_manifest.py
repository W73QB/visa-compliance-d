import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(snapshot_dir: Path) -> int:
    manifest_path = snapshot_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"[ERROR] Missing manifest: {manifest_path}")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    errors = 0
    for entry in manifest.get("files", []):
        rel = entry.get("path")
        expected = entry.get("sha256")
        if not rel or not expected:
            print("[ERROR] manifest entry missing path/sha256")
            errors += 1
            continue
        path = snapshot_dir / rel
        if not path.exists():
            print(f"[ERROR] Missing file: {rel}")
            errors += 1
            continue
        actual = sha256(path)
        if actual.lower() != str(expected).lower():
            print(f"[ERROR] SHA mismatch: {rel}")
            errors += 1

    if errors:
        print(f"[FAIL] {errors} error(s) found")
        return 1

    print("[OK] manifest verified")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-dir", required=True)
    args = parser.parse_args()
    sys.exit(verify(Path(args.snapshot_dir)))


if __name__ == "__main__":
    main()
