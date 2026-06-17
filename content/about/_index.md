---
title: "About"
description: "What VisaFact is, who runs it, and how our evidence-based visa insurance compliance checker works."
date: 2026-01-15
lastmod: 2026-06-17
---

## What VisaFact is

VisaFact is an independent, evidence-based reference that compares official visa health-insurance requirements against insurance product specifications. For each visa route we record what the authority actually requires, then a rule engine compares those requirements to documented product facts and returns a clear status: GREEN, YELLOW, RED, UNKNOWN, or NOT_REQUIRED.

The site is operated by the VisaFact team as an informational project. It is not a visa agency, an insurer, or a broker, and it does not sell insurance.

## Our core principle: evidence before answers

Every requirement and every product fact is backed by a primary source. If a detail is not stated in an official source, we mark it UNKNOWN rather than guessing. We would rather say "unknown" than be wrong.

In practice this means:

- **Requirements** come from primary government sources (ministries, consulates, official gazettes, immigration authorities). We store each source as a byte-exact snapshot and verify it with a SHA-256 hash, so the wording we encode can be traced to the exact document we read.
- **We encode only what the source states verbatim.** We do not infer coverage amounts, territories, or conditions that an official document leaves out.
- **Product facts** come from each insurer's own published policy or coverage documentation, quoted with a locator.

## How the statuses work

- **GREEN** — the product's documented facts satisfy every modeled requirement for that route.
- **YELLOW** — an operational caution (for example, a monthly subscription that can lapse before a stay ends).
- **RED** — a documented requirement is not met.
- **UNKNOWN** — a requirement or product detail lacks an official source, so no claim is made.
- **NOT_REQUIRED** — the authority does not require insurance for that route.

Read the full logic on the [Methodology](/methodology/) page.

## Independence

Compliance results are generated from sources and rules, not from commercial relationships. Some pages contain affiliate links, and they appear only after results. An affiliate link never changes a status. See our [Affiliate Disclosure](/affiliate-disclosure/) for details.

## Not legal advice

VisaFact provides informational, evidence-based snapshots. It is not legal advice. Always confirm current requirements with the official authority before you apply. See the [Disclaimer](/disclaimer/).

## Contact

Questions, corrections, or a source that looks out of date? Email **support@visafact.org** or see the [Contact](/contact/) page.
