#!/usr/bin/env python3
import json
from pathlib import Path
import argparse

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def audit_visas():
    rows = []
    for path in sorted(Path("data/visas").rglob("visa_facts.json")):
        data = load_json(path)
        vid = data.get("id") or path.parent.as_posix()
        requirements = data.get("requirements", [])
        missing_keys = []
        with_evidence = 0
        for req in requirements:
            evidence = req.get("evidence") or []
            if evidence:
                with_evidence += 1
            else:
                missing_keys.append(req.get("key"))
        source_ids = sorted({s.get("source_id") for s in data.get("sources", []) if s.get("source_id")})
        rows.append({
            "id": vid,
            "path": str(path),
            "total_requirements": len(requirements),
            "requirements_with_evidence": with_evidence,
            "missing_requirements": missing_keys,
            "source_ids": source_ids,
        })
    return rows


def audit_products():
    rows = []
    for path in sorted(Path("data/products").rglob("product_facts.json")):
        data = load_json(path)
        pid = data.get("id") or path.parent.as_posix()
        evidence = data.get("evidence") or []
        source_ids = sorted({e.get("source_id") for e in evidence if isinstance(e, dict) and e.get("source_id")})
        rows.append({
            "id": pid,
            "path": str(path),
            "evidence_count": len(evidence),
            "missing_evidence": len(evidence) == 0,
            "source_ids": source_ids,
        })
    return rows


def render_markdown(visas, products):
    lines = []
    lines.append("# Evidence Gap Report")
    lines.append("")
    lines.append("## Per Visa Route")
    lines.append("")
    for row in visas:
        lines.append(f"### {row['id']}")
        lines.append(f"- Path: `{row['path']}`")
        lines.append(f"- Total requirements: {row['total_requirements']}")
        lines.append(f"- Requirements with evidence: {row['requirements_with_evidence']}")
        if row["missing_requirements"]:
            missing = ", ".join([m for m in row["missing_requirements"] if m])
            lines.append(f"- Missing evidence for: {missing}")
        else:
            lines.append("- Missing evidence for: None")
        if row["source_ids"]:
            lines.append(f"- Sources: {', '.join(row['source_ids'])}")
        else:
            lines.append("- Sources: None")
        lines.append("")

    lines.append("## Per Product")
    lines.append("")
    for row in products:
        lines.append(f"### {row['id']}")
        lines.append(f"- Path: `{row['path']}`")
        lines.append(f"- Evidence items: {row['evidence_count']}")
        if row["missing_evidence"]:
            lines.append("- Missing evidence: Yes")
        else:
            lines.append("- Missing evidence: No")
        if row["source_ids"]:
            lines.append(f"- Sources: {', '.join(row['source_ids'])}")
        else:
            lines.append("- Sources: None")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Audit evidence gaps in visa and product facts.")
    parser.add_argument("--output", help="Write markdown report to path.")
    args = parser.parse_args()

    visas = audit_visas()
    products = audit_products()
    report = render_markdown(visas, products)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
