import json
import sys
import hashlib
from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"
SOURCES = ROOT / "sources"

visa_schema = json.loads((SCHEMAS / "visa_facts.schema.json").read_text(encoding="utf-8"))
product_schema = json.loads((SCHEMAS / "product_facts.schema.json").read_text(encoding="utf-8"))

errors = 0

def load_sources():
    sources_by_id = {}
    for path in SOURCES.rglob("*.meta.json"):
        try:
            meta = json.loads(path.read_text(encoding="utf-8"))
            source_id = meta.get("source_id")
            if source_id:
                sources_by_id[source_id] = meta
        except Exception:
            continue
    return sources_by_id

def check_product_sources(data, path, sources_by_id):
    global errors
    evidence_items = []
    evidence_items.extend(data.get("evidence", []))
    specs = data.get("specs", {})
    for facts in (specs.get("jurisdiction_facts") or {}).values():
        evidence_items.extend(facts.get("evidence", []))

    for ev in evidence_items:
        source_id = ev.get("source_id")
        if not source_id:
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", "Missing source_id in product evidence.")
            errors += 1
            continue
        meta = sources_by_id.get(source_id)
        if not meta:
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", f"Missing source metadata for source_id: {source_id}")
            errors += 1
            continue
        sha = meta.get("sha256")
        if not sha:
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", f"Missing sha256 for source_id: {source_id}")
            errors += 1
            continue
        local_path = meta.get("local_path")
        if not local_path:
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", f"Missing local_path for source_id: {source_id}")
            errors += 1
            continue
        full_path = ROOT / local_path
        if not full_path.exists():
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", f"Local source file not found for source_id: {source_id} ({local_path})")
            errors += 1
            continue
        try:
            digest = hashlib.sha256(full_path.read_bytes()).hexdigest()
        except Exception as e:
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", f"Failed to read local source file for source_id: {source_id} ({e})")
            errors += 1
            continue
        if digest.lower() != str(sha).lower():
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", f"SHA256 mismatch for source_id: {source_id}")
            errors += 1

def validate_files(folder, schema, label, sources_by_id=None):
    global errors
    for path in folder.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            validate(instance=data, schema=schema)
            print(f"[OK] {label}: {path}")
            if label == "ProductFacts" and sources_by_id is not None:
                check_product_sources(data, path, sources_by_id)
        except ValidationError as e:
            print(f"[ERROR] {label}: {path}")
            print("  ", e.message)
            errors += 1
        except Exception as e:
            print(f"[ERROR] {label}: {path}")
            print("  ", str(e))
            errors += 1

sources_by_id = load_sources()
validate_files(DATA / "visas", visa_schema, "VisaFacts")
validate_files(DATA / "products", product_schema, "ProductFacts", sources_by_id)

if errors > 0:
    print(f"\n[FAIL] {errors} error(s) found")
    sys.exit(1)
else:
    print("\nAll data files valid.")
    sys.exit(0)
