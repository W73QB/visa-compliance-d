import json
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("SMOKE_ROOT", Path(__file__).parent.parent))
INDEX_PATH = Path(os.environ.get("SMOKE_INDEX_PATH", ROOT / "data" / "ui_index.json"))


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not INDEX_PATH.exists():
        fail(f"Missing ui_index.json at {INDEX_PATH}")

    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    mappings = data.get("mappings", [])
    sources_by_id = data.get("sources_by_id", {})

    if not mappings:
        fail("No mappings found in ui_index.json")

    chosen = None
    for mapping in mappings:
        for reason in mapping.get("reasons", []) or []:
            if reason.get("evidence"):
                chosen = mapping
                break
        if chosen:
            break

    if not chosen:
        fail("No mapping with evidence found")

    for reason in chosen.get("reasons", []) or []:
        for ev in reason.get("evidence", []) or []:
            source_id = ev.get("source_id")
            if not source_id:
                fail("Evidence missing source_id")
            meta = sources_by_id.get(source_id)
            if not meta:
                fail(f"Missing sources_by_id for {source_id}")
            local_path = meta.get("local_path")
            if not local_path:
                fail(f"Missing local_path for {source_id}")
            evidence_path = ROOT / local_path
            if not evidence_path.exists():
                fail(f"Evidence file not found: {evidence_path}")

    print("Smoke check passed")


if __name__ == "__main__":
    main()
