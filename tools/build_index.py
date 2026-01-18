import json
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"
MAPPINGS = ROOT / "data" / "mappings"
OFFERS = ROOT / "data" / "offers"
SOURCES = ROOT / "sources"
OUT = ROOT / "data" / "ui_index.json"
SOURCE_STATUS = ROOT / "data" / "source_status.json"


def load_all(folder):
    files = []
    for p in sorted(folder.rglob("*.json")):
        if p.name.startswith("."):
            continue
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files


def load_offers(folder):
    offers = []
    for p in sorted(folder.rglob("*.json")):
        if p.name.startswith("."):
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        offers.extend(data.get("offers", []))
    return offers


def load_sources(folder):
    sources = {}
    for p in sorted(folder.rglob("*.meta.json")):
        if p.name.startswith("."):
            continue
        meta = json.loads(p.read_text(encoding="utf-8"))
        source_id = meta.get("source_id")
        if source_id:
            sources[source_id] = meta
    return sources


def load_source_status(path: Path) -> dict:
    if not path.exists():
        return {"checked_at": None, "needs_review_source_ids": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"checked_at": None, "needs_review_source_ids": []}


def last_verified_for_mapping(path: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        date_str = result.stdout.strip()
        return date_str or ""
    except Exception:
        return ""


print("Loading data...")
visas = sorted(load_all(VISAS), key=lambda v: v.get("id", ""))
products = sorted(load_all(PRODUCTS), key=lambda p: p.get("id", ""))

mappings = []
for path in sorted(MAPPINGS.rglob("*.json")):
    if path.name.startswith("."):
        continue
    data = json.loads(path.read_text(encoding="utf-8"))
    data["last_verified"] = last_verified_for_mapping(path)
    mappings.append(data)

mappings = sorted(mappings, key=lambda m: (m.get("visa_id", ""), m.get("product_id", "")))

sources_by_id = load_sources(SOURCES)

print(f"Loaded {len(visas)} visas, {len(products)} products, {len(mappings)} mappings.")

offers = load_offers(OFFERS) if OFFERS.exists() else []
offers_by_product = {o.get("product_id"): o for o in offers if o.get("product_id")}

source_status = load_source_status(SOURCE_STATUS)

data = {
    "built_at": datetime.now(timezone.utc).isoformat(),
    "snapshot_id": os.environ.get("SNAPSHOT_ID") or datetime.now(timezone.utc).date().isoformat(),
    "visas": visas,
    "products": products,
    "mappings": mappings,
    "offers": offers,
    "offers_by_product": offers_by_product,
    "sources_by_id": sources_by_id,
    "source_status": source_status,
}

OUT.write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"Index written to {OUT}")
