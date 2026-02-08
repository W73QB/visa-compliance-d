#!/usr/bin/env python3
"""
Generate baseline audit for 12-week traffic plan Task 1.
Outputs:
1. Content completion matrix (word counts + editorial targets)
2. Monetization eligibility matrix (Genki compliance per route)
3. Prioritization list (top 6 pages to update)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).parent.parent

# Editorial word count targets from plan
EDITORIAL_TARGETS = {
    # Route posts
    "content/posts/spain-dnv-insurance/index.md": [900, 1200],
    "content/posts/portugal-dnv-insurance.md": [450, 700],  # Evidence thin
    "content/posts/germany-freelance-insurance.md": [900, 1200],
    "content/posts/thailand-dtv-insurance.md": [900, 1200],
    "content/posts/malta-nomad-insurance.md": [900, 1200],
    "content/posts/costa-rica-dn-insurance.md": [900, 1200],
    # Comparison/rejected posts
    "content/posts/safetywing-spain-dnv-rejected.md": [1000, 1400],
    "content/posts/safetywing-vs-worldnomads-vs-genki.md": [1000, 1400],
    # Regional hubs
    "content/posts/digital-nomad-insurance-europe.md": [900, 1200],
    "content/posts/digital-nomad-insurance-asia.md": [900, 1200],
    "content/posts/digital-nomad-insurance-americas.md": [900, 1200],
    # Trap posts
    "content/traps/germany-travel-insurance-rejected.md": [700, 900],
    "content/traps/spain-dnv-coverage-cap-trap.md": [700, 900],
    "content/traps/spain-dnv-insurance-mistakes.md": [700, 900],
    "content/traps/malta-nomad-monthly-payments.md": [700, 900],
    # Visa route pages
    "content/visas/spain/digital-nomad-visa/consulate-via-bls-london/index.md": [
        900,
        1300,
    ],
    "content/visas/germany/freelance-visa-national-d/embassy-london/index.md": [
        900,
        1300,
    ],
    "content/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/index.md": [
        900,
        1300,
    ],
    "content/visas/costa-rica/digital-nomad-visa/executive-decree-43619/index.md": [
        900,
        1300,
    ],
    "content/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/index.md": [900, 1300],
    "content/visas/malta/nomad-residence-permit/residency-malta-agency/index.md": [
        900,
        1300,
    ],
    # Guides
    "content/guides/compliance-status-meaning.md": [400, 700],
    "content/guides/how-to-choose-dnv-insurance.md": [400, 700],
    "content/guides/how-to-read-results.md": [400, 700],
    "content/guides/schengen-30000-insurance.md": [400, 700],
}


def word_count(body: str) -> int:
    """Reuse word count logic from seo_audit.py"""
    body = re.sub(r"[`*_>#\[\]()-]", " ", body)
    words = re.findall(r"\b\w+\b", body)
    return len(words)


def split_frontmatter(text: str) -> Tuple[str, str]:
    """Split frontmatter from body"""
    text = text.lstrip("\ufeff")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def get_content_stats(file_path: Path) -> Dict:
    """Get word count and editorial status for a file"""
    if not file_path.exists():
        return {
            "exists": False,
            "word_count": 0,
            "editorial_min": 0,
            "editorial_max": 0,
            "gap_to_min": 0,
            "status": "MISSING",
        }

    text = file_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    wc = word_count(body)

    rel_path = str(file_path.relative_to(ROOT))
    min_wc, max_wc = EDITORIAL_TARGETS.get(rel_path, [0, 0])

    if wc < min_wc:
        status = "FAIL"
    elif wc > max_wc:
        status = "OVER"
    else:
        status = "PASS"

    return {
        "exists": True,
        "word_count": wc,
        "editorial_min": min_wc,
        "editorial_max": max_wc,
        "gap_to_min": max(0, min_wc - wc),
        "status": status,
    }


def build_monetization_matrix() -> Dict:
    """Build monetization eligibility matrix from ui_index.json"""
    ui_index_path = ROOT / "data" / "ui_index.json"
    offers_path = ROOT / "data" / "offers" / "offers.json"

    ui_index = json.loads(ui_index_path.read_text(encoding="utf-8"))
    offers = json.loads(offers_path.read_text(encoding="utf-8"))

    # Extract affiliate product IDs
    affiliate_products = {
        offer["product_id"]: offer
        for offer in offers["offers"]
        if "Paid link" in offer.get("disclosure", "")
    }

    # Build matrix: visa_id -> {product_id -> status}
    matrix = {}
    for mapping in ui_index["mappings"]:
        visa_id = mapping["visa_id"]
        product_id = mapping["product_id"]
        status = mapping["status"]

        if visa_id not in matrix:
            matrix[visa_id] = {}

        matrix[visa_id][product_id] = {
            "status": status,
            "is_affiliate": product_id in affiliate_products,
            "affiliate_eligible": (
                product_id in affiliate_products and status in ["GREEN", "YELLOW"]
            ),
        }

    return matrix


def calculate_priority_score(file_path: Path, stats: Dict, monetization: Dict) -> float:
    """
    Proxy scoring for prioritization (no GSC data available).

    Factors:
    - Word count gap to editorial target (higher = more work needed)
    - Route importance (visa route pages > posts > guides/traps)
    - Evidence density (manual flag for Portugal = lower priority)
    - Monetization potential (Genki compliant routes = higher priority)
    """
    rel_path = str(file_path.relative_to(ROOT))
    score = 0.0

    # Gap score (0-100): higher gap = higher priority
    if stats["editorial_min"] > 0:
        gap_ratio = stats["gap_to_min"] / stats["editorial_min"]
        score += min(100, gap_ratio * 100)

    # Route importance (0-50)
    if "content/visas/" in rel_path:
        score += 50  # Highest: visa route pages
    elif "content/posts/" in rel_path:
        if "insurance" in rel_path and any(
            country in rel_path
            for country in [
                "spain",
                "germany",
                "portugal",
                "thailand",
                "malta",
                "costa-rica",
            ]
        ):
            score += 40  # Route posts
        elif "comparison" in rel_path or "rejected" in rel_path:
            score += 35  # Comparison/rejected
        else:
            score += 30  # Regional hubs
    elif "content/traps/" in rel_path:
        score += 20  # Traps
    elif "content/guides/" in rel_path:
        score += 10  # Guides

    # Evidence density penalty (Portugal = thin evidence)
    if "portugal" in rel_path.lower():
        score -= 20

    # Monetization boost (Genki-compliant routes)
    # Map file paths to visa IDs
    visa_mapping = {
        "spain-dnv": "ES_DNV_BLS_LONDON_2026",
        "germany-freelance": "DE_FREELANCE_EMBASSY_LONDON_2026",
        "portugal-dnv": "PT_DNV_VFS_CHINA_2026",
        "costa-rica-dn": "CR_DN_DECREE_43619_2026",
        "thailand-dtv": "TH_DTV_MFA_2026",
        "malta-nomad": "MT_NOMAD_RESIDENCY_2026",
    }

    for key, visa_id in visa_mapping.items():
        if key in rel_path:
            if visa_id in monetization:
                genki_data = monetization[visa_id].get("GENKI_TRAVELER_2026", {})
                if genki_data.get("affiliate_eligible"):
                    score += 25  # Monetization boost
            break

    return score


def main():
    # 1. Build content completion matrix
    print("=" * 80)
    print("CONTENT COMPLETION MATRIX")
    print("=" * 80)
    print(f"{'File':<70} {'Words':>6} {'Min':>5} {'Max':>5} {'Gap':>5} {'Status':>6}")
    print("-" * 80)

    all_stats = {}
    for rel_path in sorted(EDITORIAL_TARGETS.keys()):
        file_path = ROOT / rel_path
        stats = get_content_stats(file_path)
        all_stats[rel_path] = stats

        print(
            f"{rel_path:<70} "
            f"{stats['word_count']:>6} "
            f"{stats['editorial_min']:>5} "
            f"{stats['editorial_max']:>5} "
            f"{stats['gap_to_min']:>5} "
            f"{stats['status']:>6}"
        )

    # 2. Build monetization eligibility matrix
    print("\n" + "=" * 80)
    print("MONETIZATION ELIGIBILITY MATRIX")
    print("=" * 80)
    print("Route: Genki Status / Affiliate Eligible")
    print("-" * 80)

    monetization = build_monetization_matrix()
    for visa_id in sorted(monetization.keys()):
        genki_data = monetization[visa_id].get("GENKI_TRAVELER_2026", {})
        status = genki_data.get("status", "N/A")
        eligible = "YES" if genki_data.get("affiliate_eligible") else "NO"
        print(f"{visa_id:<40} {status:>12} / {eligible:>3}")

    # 3. Generate prioritization list
    print("\n" + "=" * 80)
    print("PRIORITIZATION LIST (Top 6 Pages)")
    print("=" * 80)
    print(f"{'Rank':<5} {'Score':>6} {'File':<70}")
    print("-" * 80)

    priorities = []
    for rel_path, stats in all_stats.items():
        if stats["status"] == "FAIL":  # Only prioritize files that need work
            file_path = ROOT / rel_path
            score = calculate_priority_score(file_path, stats, monetization)
            priorities.append((score, rel_path, stats))

    priorities.sort(reverse=True, key=lambda x: x[0])

    for rank, (score, rel_path, stats) in enumerate(priorities[:6], start=1):
        print(f"{rank:<5} {score:>6.1f} {rel_path:<70}")

    # 4. Save editorial targets JSON
    targets_json_path = ROOT / "tools" / "editorial_targets.json"
    targets_json_path.write_text(
        json.dumps(EDITORIAL_TARGETS, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"\n✓ Saved editorial targets to {targets_json_path}")

    # 5. Summary stats
    total = len(all_stats)
    passed = sum(1 for s in all_stats.values() if s["status"] == "PASS")
    failed = sum(1 for s in all_stats.values() if s["status"] == "FAIL")
    over = sum(1 for s in all_stats.values() if s["status"] == "OVER")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files: {total}")
    print(f"  PASS:  {passed} ({passed / total * 100:.1f}%)")
    print(f"  FAIL:  {failed} ({failed / total * 100:.1f}%)")
    print(f"  OVER:  {over} ({over / total * 100:.1f}%)")
    print(f"\nTop 6 pages to rewrite (ranked by priority score):")
    for rank, (score, rel_path, _) in enumerate(priorities[:6], start=1):
        print(f"  {rank}. {rel_path}")


if __name__ == "__main__":
    main()
