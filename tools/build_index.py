import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"
MAPPINGS = ROOT / "data" / "mappings"
OUT = ROOT / "data" / "ui_index.json"

def load_all(folder):
    files = []
    for p in folder.rglob("*.json"):
        if p.name.startswith("."): continue
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files

print("Loading data...")
visas = load_all(VISAS)
products = load_all(PRODUCTS)
mappings = load_all(MAPPINGS)

print(f"Loaded {len(visas)} visas, {len(products)} products, {len(mappings)} mappings.")

data = {
    "built_at": datetime.utcnow().isoformat() + "Z",
    "visas": visas,
    "products": products,
    "mappings": mappings
}

OUT.write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"Index written to {OUT}")
