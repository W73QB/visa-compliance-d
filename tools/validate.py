import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"
SOURCES = ROOT / "sources"

visa_schema = json.loads((SCHEMAS / "visa_facts.schema.json").read_text(encoding="utf-8"))
product_schema = json.loads((SCHEMAS / "product_facts.schema.json").read_text(encoding="utf-8"))
offers_schema = json.loads((SCHEMAS / "offers.schema.json").read_text(encoding="utf-8"))

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

def sha256_for_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".json"}:
        text = path.read_text(encoding="utf-8", errors="replace")
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return hashlib.sha256(path.read_bytes()).hexdigest()

BANNED_OFFER_WORDS = [
    "best",
    "recommend",
    "recommended",
    "guarantee",
    "guaranteed",
    "100%",
    "approved",
    "surely",
]


def check_offer_language(data, path):
    global errors
    for offer in data.get("offers", []):
        text = (offer.get("label", "") + " " + offer.get("disclosure", "")).lower()
        for word in BANNED_OFFER_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", text):
                print(f"[ERROR] Offers: {path}")
                print("  ", f"Banned word in offer: {word}")
                errors += 1
                break

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
            digest = sha256_for_path(full_path)
        except Exception as e:
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", f"Failed to read local source file for source_id: {source_id} ({e})")
            errors += 1
            continue
        if digest.lower() != str(sha).lower():
            print(f"[ERROR] ProductFacts: {path}")
            print("  ", f"SHA256 mismatch for source_id: {source_id}")
            errors += 1

def validate_file(path, schema, label, sources_by_id=None):
    global errors
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        validate(instance=data, schema=schema)
        print(f"[OK] {label}: {path}")
        if label == "ProductFacts" and sources_by_id is not None:
            check_product_sources(data, path, sources_by_id)
        if label == "Offers":
            check_offer_language(data, path)
    except ValidationError as e:
        print(f"[ERROR] {label}: {path}")
        print("  ", e.message)
        errors += 1
    except Exception as e:
        print(f"[ERROR] {label}: {path}")
        print("  ", str(e))
        errors += 1

def validate_files(folder, schema, label, sources_by_id=None):
    for path in folder.rglob("*.json"):
        validate_file(path, schema, label, sources_by_id)

parser = argparse.ArgumentParser()
parser.add_argument("--visa", type=str, help="Path to a single VisaFacts JSON to validate")
parser.add_argument("--product", type=str, help="Path to a single ProductFacts JSON to validate")
parser.add_argument("--offers", type=str, help="Path to a single Offers JSON to validate")
args = parser.parse_args()

sources_by_id = load_sources()
if args.visa:
    validate_file(Path(args.visa), visa_schema, "VisaFacts")
elif args.product:
    validate_file(Path(args.product), product_schema, "ProductFacts", sources_by_id)
elif args.offers:
    validate_file(Path(args.offers), offers_schema, "Offers")
else:
    validate_files(DATA / "visas", visa_schema, "VisaFacts")
    validate_files(DATA / "products", product_schema, "ProductFacts", sources_by_id)
    if (DATA / "offers").exists():
        validate_files(DATA / "offers", offers_schema, "Offers")

if errors > 0:
    print(f"\n[FAIL] {errors} error(s) found")
    sys.exit(1)
else:
    print("\nAll data files valid.")
    sys.exit(0)
