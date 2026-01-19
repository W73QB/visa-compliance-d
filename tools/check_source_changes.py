import argparse
import hashlib
import json
import sys
import urllib.request
from datetime import datetime
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
    parser.add_argument("--write-status", default="")
    parser.add_argument("--report-md", default="")
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

    checked_at = datetime.utcnow().isoformat() + "Z"
    report = {"checked_at": checked_at, "changed": changed}
    output = json.dumps(report, indent=2)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
    else:
        print(output)

    if args.write_status:
        status_path = Path(args.write_status)
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status = {
            "checked_at": checked_at,
            "needs_review_source_ids": [item["source_id"] for item in changed]
        }
        status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")

    if args.report_md:
        report_path = Path(args.report_md)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        if changed:
            lines_md = [
                "# Source Monitor Report",
                "",
                f"Checked at: {checked_at}",
                "",
                "## Changed Sources",
                "",
            ]
            for item in changed:
                lines_md.append(f"- **{item['source_id']}** | {item['url']} | `{item['sha256']}`")
        else:
            lines_md = [
                "# Source Monitor Report",
                "",
                f"Checked at: {checked_at}",
                "",
                "No changes detected.",
            ]
        report_path.write_text("\n".join(lines_md) + "\n", encoding="utf-8")

    sys.exit(0)


if __name__ == "__main__":
    main()
