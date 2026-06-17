#!/usr/bin/env python3
"""Generate the linkable 'visa insurance requirements by country' comparison page.

Reads every data/visas/**/visa_facts.json and emits
content/visa-insurance-requirements/_index.md: a single comprehensive,
evidence-based comparison table + citable summary stats. Re-run when routes
change. Route links point to the generated hub pages (slug rules mirror
build_content_hubs.slugify), validated by check_internal_links.py.
"""
import json
import re
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "content", "visa-insurance-requirements", "_index.md")
SNAPSHOT = os.environ.get("SNAPSHOT_ID", "2026-06-13")


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "unknown"


def fmt_amount(val, ccy):
    try:
        n = "{:,}".format(int(val))
    except Exception:
        n = str(val)
    return f"{n} {ccy}".strip()


def load_routes():
    rows = []
    for f in glob.glob(os.path.join(ROOT, "data", "visas", "**", "visa_facts.json"), recursive=True):
        d = json.load(open(f, encoding="utf-8"))
        reqs = {r["key"]: r for r in d.get("requirements", [])}
        mandatory = reqs.get("insurance.mandatory", {}).get("value", True)
        minc = reqs.get("insurance.min_coverage")
        min_str = fmt_amount(minc["value"], minc.get("currency", "")) if minc else "—"
        tags = []
        if reqs.get("insurance.must_cover_full_period", {}).get("value"):
            tags.append("full stay")
        if reqs.get("insurance.eu_licensed_insurer", {}).get("value"):
            tags.append("EU-licensed insurer")
        if any(k.startswith("insurance.authorized_in") for k in reqs):
            tags.append("valid-in-country insurer")
        if reqs.get("insurance.comprehensive", {}).get("value"):
            tags.append("comprehensive")
        if reqs.get("insurance.unlimited_coverage", {}).get("value"):
            tags.append("unlimited")
        if reqs.get("insurance.covers_public_health_system_risks", {}).get("value"):
            tags.append("public-health-equivalent")
        if reqs.get("insurance.no_deductible", {}).get("value") or reqs.get("insurance.no_copayment", {}).get("value"):
            tags.append("no deductible/copay")
        if reqs.get("insurance.travel_insurance_accepted", {}).get("value") is False:
            tags.append("travel insurance not accepted")
        hub = "/visas/{}/{}/{}/".format(
            slugify(d["country"]), slugify(d["visa_name"]), slugify(d["route"]))
        rows.append({
            "country": d["country"],
            "visa": d["visa_name"],
            "required": bool(mandatory),
            "min": min_str if mandatory else "—",
            "tags": ", ".join(tags) if (mandatory and tags) else ("—" if mandatory else "not required"),
            "hub": hub,
        })
    rows.sort(key=lambda r: (r["country"], r["visa"]))
    return rows


def main():
    rows = load_routes()
    countries = sorted({r["country"] for r in rows})
    n_routes = len(rows)
    n_countries = len(countries)
    n_required = sum(1 for r in rows if r["required"])
    n_not = n_routes - n_required
    n_min = sum(1 for r in rows if r["required"] and r["min"] != "—")
    n_full = sum(1 for r in rows if "full stay" in r["tags"])
    n_terr = sum(1 for r in rows if "valid-in-country insurer" in r["tags"] or "EU-licensed insurer" in r["tags"])

    lines = []
    lines.append("---")
    lines.append('title: "Visa health insurance requirements by country (2026, evidence-based)"')
    lines.append('description: "A comprehensive, source-backed comparison of health insurance requirements for {} long-stay and digital-nomad visa routes across {} countries."'.format(n_routes, n_countries))
    lines.append("date: 2026-06-16")
    lines.append("lastmod: 2026-06-16")
    lines.append("---")
    lines.append("")
    lines.append("This page compares the official health-insurance requirements for **{} long-stay, digital-nomad and residence visa routes across {} countries**. Every entry is built from a primary government source, stored as a byte-exact snapshot and verified with a SHA-256 hash. Where an official source does not state a detail, we mark it UNKNOWN rather than guess.".format(n_routes, n_countries))
    lines.append("")
    lines.append("## Key findings")
    lines.append("")
    lines.append("- **{} of {} routes require health insurance**; {} do not list it as a required document.".format(n_required, n_routes, n_not))
    lines.append("- **{} routes specify a minimum coverage amount.** Stated minimums range from EUR 5,792 (Lithuania national D visa) upward; Spain's digital-nomad and non-lucrative visas instead require *unlimited* cover from an insurer authorized in Spain.".format(n_min))
    lines.append("- **{} routes restrict the insurer or territory** — the policy must be valid in the destination, or issued by a locally-authorized or EU-licensed insurer.".format(n_terr))
    lines.append("- **{} routes require the policy to cover the full period of stay**, which rules out subscriptions that can lapse mid-stay.".format(n_full))
    lines.append("- Stated amounts appear in several currencies (EUR, USD, GBP, JPY, KRW, ISK), so a like-for-like comparison needs currency conversion.")
    lines.append("")
    lines.append("## Requirements by country")
    lines.append("")
    lines.append("| Country | Visa / route | Insurance | Min. coverage | Key conditions |")
    lines.append("| --- | --- | --- | --- | --- |")
    for r in rows:
        req = "Required" if r["required"] else "Not required"
        lines.append("| {} | [{}]({}) | {} | {} | {} |".format(
            r["country"], r["visa"], r["hub"], req, r["min"], r["tags"]))
    lines.append("")
    lines.append("## How we compile this")
    lines.append("")
    lines.append("Each requirement is taken from an official authority source (a ministry, consulate, immigration department or official gazette). We store the exact document, hash it, and encode only the requirements the source states verbatim. A rule engine then compares those requirements to insurance product facts and returns a status (GREEN, YELLOW, RED, UNKNOWN, or NOT_REQUIRED). See the [methodology](/methodology/) for the full logic and the [compliance checker](/ui/) to test a specific policy.")
    lines.append("")
    lines.append("## Use or cite this data")
    lines.append("")
    lines.append("You are welcome to cite these figures or link to this page. Please attribute VisaFact and link to <https://visafact.org/visa-insurance-requirements/>. Requirements change, so each row links to the route page where you can see the source and verification date.")
    lines.append("")
    lines.append("## Frequently asked questions")
    lines.append("")
    lines.append("**Which visas need health insurance?**  ")
    lines.append("Most long-stay and digital-nomad routes do: {} of the {} routes here require it. A few (for example Thailand's DTV) do not list insurance as a required document.".format(n_required, n_routes))
    lines.append("")
    lines.append("**Is there a standard minimum amount?**  ")
    lines.append("No. Minimums differ by country and many routes state no figure at all. Where an amount is stated it ranges from EUR 5,792 upward, and Spain requires unlimited cover.")
    lines.append("")
    lines.append("**Is travel insurance enough?**  ")
    lines.append("It depends on the route. Some accept travel medical insurance; others (such as Spain and Germany) require comprehensive health insurance and reject travel policies. Check the specific route.")
    lines.append("")
    lines.append("## Disclaimer")
    lines.append("")
    lines.append("Not legal advice. This is an evidence-based snapshot; always confirm current requirements with the official authority before you apply.")
    lines.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print("Wrote {} ({} routes / {} countries)".format(OUT, n_routes, n_countries))


if __name__ == "__main__":
    main()
