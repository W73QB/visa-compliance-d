import json
import sys
from pathlib import Path
from jsonschema import validate
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"

visa_schema = json.loads((SCHEMAS / "visa_facts.schema.json").read_text(encoding="utf-8"))
product_schema = json.loads((SCHEMAS / "product_facts.schema.json").read_text(encoding="utf-8"))

errors = 0

def validate_files(folder, schema, label):
    global errors
    for path in folder.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            validate(instance=data, schema=schema)
            print(f"[OK] {label}: {path}")
        except ValidationError as e:
            print(f"[ERROR] {label}: {path}")
            print("  ", e.message)
            errors += 1
        except Exception as e:
            print(f"[ERROR] {label}: {path}")
            print("  ", str(e))
            errors += 1

validate_files(DATA / "visas", visa_schema, "VisaFacts")
validate_files(DATA / "products", product_schema, "ProductFacts")

if errors > 0:
    print(f"\n❌ {errors} error(s) found")
    sys.exit(1)
else:
    print("\n✅ All files valid")
    sys.exit(0)
