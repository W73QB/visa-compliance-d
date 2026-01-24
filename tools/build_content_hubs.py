#!/usr/bin/env python3
"""Generate visa content hubs from visa_facts.json data."""

from pathlib import Path
import json
import re
import os
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
SOURCES = ROOT / "sources"
OUT = ROOT / "content" / "visas"


def slugify(value: str) -> str:
    """Convert string to URL-safe slug."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "unknown"


def load_sources() -> dict:
    """Load all source metadata from sources/*.meta.json."""
    sources = {}
    for p in SOURCES.rglob("*.meta.json"):
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))
            source_id = meta.get("source_id")
            if source_id:
                sources[source_id] = meta
        except (json.JSONDecodeError, IOError):
            continue
    return sources


def get_lint_required_blocks(visa_id: str, visa_name: str, snapshot_id: str) -> str:
    """Return the required content blocks for lint_content.py compliance."""
    return f"""
## What the authority requires

See the requirements table above. All requirements are extracted directly from official sources with evidence excerpts.

## How we evaluate

We compare these official requirements against insurance product specifications using our automated rule engine. Each requirement is matched to a product fact with evidence.

## Check in the engine

Try the compliance checker: [Open Checker](/ui/?visa={visa_id}&snapshot={snapshot_id})

## Disclaimer

This is not legal advice. VisaFact provides evidence-based compliance checking only. Final visa decisions are made by government authorities. A GREEN result does not ensure visa approval.

## Affiliate disclosure

If affiliate links appear, they are shown only after compliance results and do not influence the compliance evaluation in any way.
"""


def get_root_lint_blocks(snapshot_id: str) -> str:
    """Return the required content blocks for root index (no specific visa)."""
    return f"""
## What the authority requires

See the requirements table above. All requirements are extracted directly from official sources with evidence excerpts.

## How we evaluate

We compare these official requirements against insurance product specifications using our automated rule engine. Each requirement is matched to a product fact with evidence.

## Check in the engine

Try the compliance checker: [Open Checker](/ui/?snapshot={snapshot_id})

## Disclaimer

This is not legal advice. VisaFact provides evidence-based compliance checking only. Final visa decisions are made by government authorities. A GREEN result does not ensure visa approval.

## Affiliate disclosure

If affiliate links appear, they are shown only after compliance results and do not influence the compliance evaluation in any way.
"""


def render_overview(country_slug: str, visa_slug: str, visa_name: str,
                    country_name: str, routes: list, snapshot_id: str) -> str:
    """Render the overview _index.md for a visa type."""
    lines = [
        "---",
        f'title: "{country_name} {visa_name}"',
        f'visa_group: "{country_slug}-{visa_slug}"',
        f'description: "Insurance requirements for {country_name} {visa_name} - evidence-based compliance checker"',
        "---",
        "",
        f"# {country_name} {visa_name} Requirements",
        "",
        "All requirements below are derived from official sources. Missing evidence means UNKNOWN.",
        "",
        "## Routes",
        "",
        "| Authority | Route | Last Verified | Details |",
        "| --- | --- | --- | --- |",
    ]

    for route in routes:
        lines.append(
            f"| {route['authority']} | {route['route']} | {route['last_verified']} | "
            f"[View requirements]({route['link']}) |"
        )

    # Add required lint blocks
    first_visa_id = routes[0]["visa_id"] if routes else f"{country_slug.upper()}_{visa_slug.upper()}"
    lines.append(get_lint_required_blocks(first_visa_id, visa_name, snapshot_id))

    lines.append("")
    lines.append('{{< vf-cta href="/ui/" label="Open Compliance Checker" >}}')
    lines.append("")

    return "\n".join(lines)


def render_root_index(groups: dict, snapshot_id: str) -> str:
    """Render the root visas index page."""
    lines = [
        "---",
        'title: "Visa Requirements"',
        'description: "Evidence-based visa insurance requirements by country and visa type"',
        "---",
        "",
        "# Visa Requirements by Country",
        "",
        "Browse requirements by country and visa type. All requirements are sourced from official evidence.",
        "",
        "## Countries",
        "",
    ]
    for (country_slug, visa_slug), routes in sorted(groups.items()):
        country_name = routes[0]["country"]
        visa_name = routes[0]["visa_name"]
        lines.append(f"- [{country_name} {visa_name}](/visas/{country_slug}/{visa_slug}/)")

    # Add required lint blocks (no visa= param for root index)
    lines.append(get_root_lint_blocks(snapshot_id))

    lines.append("")
    lines.append('{{< vf-cta href="/ui/" label="Open Compliance Checker" >}}')
    lines.append("")
    return "\n".join(lines)


def render_detail(visa: dict, sources: dict, snapshot_id: str) -> None:
    """Render a detail page for a specific visa route."""
    country_slug = slugify(visa["country"])
    visa_slug = slugify(visa["visa_name"])
    authority_slug = slugify(visa["route"])
    visa_id = visa["id"]

    # Get source IDs from visa sources array
    source_ids = [s["source_id"] for s in visa.get("sources", [])]

    lines = [
        "---",
        f'title: "{visa["country"]} {visa["visa_name"]} - {visa["route"]}"',
        f'visa_id: "{visa_id}"',
        f'last_verified: "{visa.get("last_verified", "")}"',
        f'source_ids: {json.dumps(source_ids)}',
        f'description: "Official insurance requirements for {visa["country"]} {visa["visa_name"]} via {visa["route"]}"',
        "---",
        "",
        f"# {visa['country']} {visa['visa_name']}",
        "",
        f"**Route:** {visa['route']}  ",
        f"**Authority:** {visa.get('authority', visa['route'])}  ",
        f"**Last Verified:** {visa.get('last_verified', 'Unknown')}",
        "",
        "## Requirements",
        "",
        "| Requirement | Operator | Value | Evidence |",
        "| --- | --- | --- | --- |",
    ]

    for req in visa.get("requirements", []):
        key = req.get("key", "")
        op = req.get("op", "")
        value = req.get("value", "")

        # Format value for display
        if isinstance(value, bool):
            value_str = "Yes" if value else "No"
        else:
            value_str = str(value)

        # Build evidence string
        evidence_items = []
        for ev in req.get("evidence", []):
            sid = ev.get("source_id", "")
            locator = ev.get("locator", "")
            excerpt = ev.get("excerpt", "")
            excerpt = excerpt.replace("|", "\\|").replace("\n", " ")

            # Try to get local path from sources metadata
            meta = sources.get(sid, {})
            local_path = meta.get("local_path", "")

            if local_path:
                evidence_items.append(f'*{locator}*: "{excerpt[:80]}..." ([source](/{local_path}))')
            else:
                evidence_items.append(f'*{locator}*: "{excerpt[:80]}..." (source_id: {sid})')

        evidence = " ".join(evidence_items) if evidence_items else "*No evidence recorded*"
        lines.append(f"| `{key}` | `{op}` | {value_str} | {evidence} |")

    # Add source documents section
    lines.append("")
    lines.append("## Source Documents")
    lines.append("")

    for src in visa.get("sources", []):
        sid = src.get("source_id", "")
        url = src.get("url", "")
        local_path = src.get("local_path", "")
        retrieved = src.get("retrieved_at", "")[:10] if src.get("retrieved_at") else ""

        if local_path:
            lines.append(f"- **{sid}**: [Local copy](/{local_path}) | [Original]({url}) | Retrieved: {retrieved}")
        else:
            lines.append(f"- **{sid}**: [Original]({url}) | Retrieved: {retrieved}")

    # Add required lint blocks
    lines.append(get_lint_required_blocks(visa_id, visa["visa_name"], snapshot_id))

    lines.append("")
    lines.append('{{< vf-cta href="/ui/" label="Open Compliance Checker" >}}')
    lines.append("")

    # Write file
    out_dir = OUT / country_slug / visa_slug / authority_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {out_dir / 'index.md'}")


def main():
    """Main entry point."""
    sources = load_sources()
    snapshot_id = os.environ.get("SNAPSHOT_ID") or datetime.now(timezone.utc).date().isoformat()
    visas = []

    for p in VISAS.rglob("visa_facts.json"):
        try:
            visas.append(json.loads(p.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load {p}: {e}")
            continue

    if not visas:
        print("No visa_facts.json files found.")
        return

    # Group visas by country+visa_name for overview pages
    grouped = {}
    for visa in visas:
        country_slug = slugify(visa["country"])
        visa_slug = slugify(visa["visa_name"])
        authority_slug = slugify(visa["route"])
        key = (country_slug, visa_slug)

        grouped.setdefault(key, []).append({
            "authority": visa.get("authority", visa["route"]),
            "route": visa.get("route", ""),
            "last_verified": visa.get("last_verified", ""),
            "link": f"/visas/{country_slug}/{visa_slug}/{authority_slug}/",
            "country": visa["country"],
            "visa_name": visa["visa_name"],
            "visa_id": visa["id"],
        })

        # Render detail page
        render_detail(visa, sources, snapshot_id)

    # Render overview pages
    for (country_slug, visa_slug), routes in grouped.items():
        country_name = routes[0]["country"]
        visa_name = routes[0]["visa_name"]
        out_dir = OUT / country_slug / visa_slug
        out_dir.mkdir(parents=True, exist_ok=True)

        content = render_overview(country_slug, visa_slug, visa_name, country_name, routes, snapshot_id)
        (out_dir / "_index.md").write_text(content, encoding="utf-8")
        print(f"Generated: {out_dir / '_index.md'}")

    # Render root visas index
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_index.md").write_text(render_root_index(grouped, snapshot_id), encoding="utf-8")
    print(f"Generated: {OUT / '_index.md'}")

    print(f"\nGenerated {len(visas)} detail pages and {len(grouped)} overview pages.")


if __name__ == "__main__":
    main()
