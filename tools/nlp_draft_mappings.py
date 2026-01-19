import argparse
import json
import re
from pathlib import Path


def extract_text(path: Path) -> str:
    data = path.read_bytes()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="ignore")


def find_matches(text: str):
    patterns = [
        ("deductible", re.compile(r"(deductible|excess)\s*[:=]?\s*(\d+)", re.IGNORECASE)),
        ("copay", re.compile(r"(copay|co-pay)\s*[:=]?\s*(\d+)", re.IGNORECASE)),
        ("moratorium_days", re.compile(r"(moratorium|waiting\s*period)\s*[:=]?\s*(\d+)", re.IGNORECASE)),
    ]
    changes = []
    snippets = []
    for field, regex in patterns:
        for match in regex.finditer(text):
            value = match.group(2)
            snippet = match.group(0)
            changes.append({"field": field, "value": value})
            snippets.append(snippet)
            break
    return changes, snippets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source-id", default="UNKNOWN_SOURCE")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    text = extract_text(input_path)
    suggested_changes, evidence_snippets = find_matches(text)

    payload = {
        "source_id": args.source_id,
        "suggested_changes": suggested_changes,
        "evidence_snippets": evidence_snippets,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
