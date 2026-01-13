import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"
MAPPINGS = ROOT / "data" / "mappings"
SOURCES = ROOT / "sources"
OUT = ROOT / "data" / "ui_index.json"

def load_all(folder):
    files = []
    for p in sorted(folder.rglob("*.json")):
        if p.name.startswith("."): continue
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files

def load_sources(folder):
    sources = {}
    for p in sorted(folder.rglob("*.meta.json")):
        if p.name.startswith("."): continue
        meta = json.loads(p.read_text(encoding="utf-8"))
        source_id = meta.get("source_id")
        if source_id:
            sources[source_id] = meta
    return sources

print("Loading data...")
visas = sorted(load_all(VISAS), key=lambda v: v.get("id", ""))
products = sorted(load_all(PRODUCTS), key=lambda p: p.get("id", ""))
mappings = sorted(load_all(MAPPINGS), key=lambda m: (m.get("visa_id", ""), m.get("product_id", "")))
sources_by_id = load_sources(SOURCES)

print(f"Loaded {len(visas)} visas, {len(products)} products, {len(mappings)} mappings.")

# Pre-compute maps to save client CPU
visas_by_id = {v["id"]: v for v in visas}
products_by_id = {p["id"]: p for p in products}
mappings_by_key = {f"{m['visa_id']}__{m['product_id']}": m for m in mappings}

# Pre-compute lightweight lists for dropdowns
visa_list = [{
    "id": v["id"],
    "country": v.get("country"),
    "visa_name": v.get("visa_name"),
    "route": v.get("route")
} for v in visas]

product_list = [{
    "id": p["id"],
    "provider": p.get("provider"),
    "product_name": p.get("product_name")
} for p in products]

data = {
    # Fix deprecation warning and use UTC
    "built_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "snapshot_id": os.environ.get("SNAPSHOT_ID") or datetime.now(timezone.utc).date().isoformat(),

    # Pre-computed indices
    "visas_by_id": visas_by_id,
    "products_by_id": products_by_id,
    "mappings_by_key": mappings_by_key,

    # Pre-computed lists
    "visa_list": visa_list,
    "product_list": product_list,

    "sources_by_id": sources_by_id

    # Raw lists (visas, products, mappings) removed to reduce payload size
    # ui/index.html supports this optimized shape
}

# Dump minified JSON to save bandwidth
# separators=(',', ':') removes whitespace around separators
OUT.write_text(json.dumps(data, separators=(',', ':')), encoding="utf-8")
print(f"Index written to {OUT}")
