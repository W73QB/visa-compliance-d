import json
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"
MAPPINGS = ROOT / "data" / "mappings"
OFFERS = ROOT / "data" / "offers"
SOURCES = ROOT / "sources"
OUT = ROOT / "data" / "ui_index.json"

def load_all(folder):
    files = []
    for p in sorted(folder.rglob("*.json")):
        if p.name.startswith("."): continue
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files


def load_offers(folder):
    offers = []
    for p in sorted(folder.rglob("*.json")):
        if p.name.startswith("."): continue
        data = json.loads(p.read_text(encoding="utf-8"))
        offers.extend(data.get("offers", []))
    return offers

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

offers = load_offers(OFFERS) if OFFERS.exists() else []
offers_by_product = {o.get("product_id"): o for o in offers if o.get("product_id")}

data = {
    "built_at": datetime.utcnow().isoformat() + "Z",
    "snapshot_id": os.environ.get("SNAPSHOT_ID") or datetime.utcnow().date().isoformat(),
    "visas": visas,
    "products": products,
    "mappings": mappings,
    "offers": offers,
    "offers_by_product": offers_by_product,
    "sources_by_id": sources_by_id
}

OUT.write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"Index written to {OUT}")
