import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_bytes(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=20) as resp:
        return resp.read()


def load_sources(sources_dir: Path) -> list[dict]:
    items = []
    for path in sources_dir.rglob("*.meta.json"):
        try:
            items.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return items


def resolve_fixture_bytes(fixture_dir: Path, source_id: str) -> bytes:
    path = fixture_dir / f"{source_id}.txt"
    if not path.exists():
        path = fixture_dir / f"{source_id}.bin"
    return path.read_bytes()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources-dir", default="sources")
    parser.add_argument("--fixture-dir", default="")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    sources_dir = Path(args.sources_dir)
    fixture_dir = Path(args.fixture_dir) if args.fixture_dir else None

    changed = []
    for meta in load_sources(sources_dir):
        source_id = meta.get("source_id")
        url = meta.get("url")
        expected = str(meta.get("sha256") or "")
        if not source_id or not url or not expected:
            continue
        try:
            data = resolve_fixture_bytes(fixture_dir, source_id) if fixture_dir else fetch_bytes(url)
            actual = sha256_bytes(data)
            if actual.lower() != expected.lower():
                changed.append({"source_id": source_id, "url": url, "sha256": actual})
        except Exception as exc:
            print(f"[WARN] {source_id}: {exc}")

    report = {"changed": changed}
    output = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)

    sys.exit(0)


if __name__ == "__main__":
    main()
