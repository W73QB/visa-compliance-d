"""Build compliance mappings between visas and products."""
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.engine import evaluate

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"
MAPPINGS = ROOT / "data" / "mappings"

MAPPINGS.mkdir(exist_ok=True)


def load_all(folder):
    """Load all JSON files from a folder."""
    files = []
    for p in folder.rglob("*.json"):
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files


def main():
    """Build all visa/product mappings."""
    visas = load_all(VISAS)
    products = load_all(PRODUCTS)
    
    for visa in visas:
        for product in products:
            result = evaluate(visa, product)
            out = MAPPINGS / f"{visa['id']}__{product['id']}.json"
            out.write_text(json.dumps(result, indent=2), encoding="utf-8")
            print("Built", out)


if __name__ == "__main__":
    main()
