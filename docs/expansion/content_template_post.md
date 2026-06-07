# Content Template — Hub Blog Post (Insurance Post)

_Copy-paste this template to create a new `content/posts/<country>-<visa-slug>-insurance.md`. Replace all `[BRACKET]` placeholders before publishing. The post links to the authority-level visa page; publish the visa page first._

---

```markdown
---
title: "[COUNTRY_NAME] [VISA_TYPE_SHORT] Insurance Requirements"
date: [YYYY-MM-DD]
description: "Evidence-based summary of [COUNTRY_NAME] [VISA_TYPE_SHORT] insurance requirement."
tags: ["[country-slug]", "[visa-slug]", "insurance", "compliance"]
faq:
  - question: "Is [insurance type] required for the [COUNTRY_NAME] [VISA_TYPE_SHORT]?"
    answer: "[YES/NO]. The [authority name] [checklist/requirements page] requires [type of insurance] for this route."
  - question: "What coverage must the policy include?"
    answer: "The [checklist/requirements page] requires [state exact coverage types from the authority source]."
  - question: "Does the checklist specify a minimum coverage amount?"
    answer: "[YES — the [authority] requires at least [AMOUNT]. / Not in this route's checklist. Only the coverage types are specified.]"
  - question: "Why [are / aren't] all products [GREEN / varied] in this snapshot?"
    answer: "[Explain the snapshot result in plain terms. Reference the snapshot ID. If all GREEN, explain that only the mandatory requirement is encoded and stricter attributes are not yet modeled. If mixed, explain which requirement causes RED outcomes.]"
---

## Short answer

For the [COUNTRY_NAME] [VISA_TYPE_SHORT] ([AUTHORITY_SHORT_NAME] route), the [checklist/requirements page] requires [one-sentence statement of the insurance requirement verbatim or closely paraphrased]. (Source: `[SOURCE_ID]`, [locator]; verified [YYYY-MM-DD]).

## Key findings at a glance

| Item | Value |
|---|---|
| Route | [COUNTRY_NAME] [VISA_TYPE_SHORT] ([AUTHORITY_SHORT_NAME]) |
| Evidence verified | [YYYY-MM-DD] |
| Snapshot | releases/2026-01-15 |
| GREEN / RED / UNKNOWN | [N] / [N] / [N] |

## What the authority requires

- [Requirement 1]. (Source: `[SOURCE_ID]`, locator: [page/section]; verified [YYYY-MM-DD])
- [Requirement 2]. (Source: `[SOURCE_ID]`, locator: [page/section]; verified [YYYY-MM-DD])

Normalized requirements table:

| Requirement | Source URL | Locator | Verified date |
|---|---|---|---|
| [Requirement 1 short label] | [authority_source_url] | [page/section] | [YYYY-MM-DD] |
| [Requirement 2 short label] | [authority_source_url] | [page/section] | [YYYY-MM-DD] |

## Verified requirements (PASS/FAIL/UNKNOWN)

| Requirement | Status | Evidence |
|---|---|---|
| [Requirement 1] | PASS | [SOURCE_ID], [locator] |
| [Optional requirement not stated in source] | UNKNOWN | Not stated in [SOURCE_ID] |

## How we evaluate

The checker currently encodes the mandatory insurance rule for this route. If a requirement is not explicitly stated in the source, it is treated as UNKNOWN rather than inferred. This keeps the results aligned with evidence-first rules. See /methodology/ for full logic.

## Proof package checklist

- [A valid insurance policy or certificate that explicitly states the required coverage type (e.g. [COVERAGE_TYPE])].
- [Any additional documentation the authority requires alongside the insurance certificate.]

## Common rejection traps

- [Trap 1 — state what has caused rejections based on the authority source. If no rejection data is available, omit this section rather than inventing traps.]
- [Trap 2]

## FAQ

**Q: [Question from front matter 1]**
**A:** [Answer] (Source: `[SOURCE_ID]`, [locator]; verified [YYYY-MM-DD]).

**Q: [Question from front matter 2]**
**A:** [Answer] (Source: `[SOURCE_ID]`, [locator]; verified [YYYY-MM-DD]).

**Q: [Question from front matter 3]**
**A:** [Answer]

**Q: [Question from front matter 4]**
**A:** [Answer]

## Check in the engine

Use [the compliance checker](/ui/) with the current snapshot for this route:

{{< checker_cta visa="[VISA_ID]" snapshot="releases/2026-01-15" >}}

## Related reading

- [[COUNTRY_NAME] [VISA_TYPE_SHORT] route page (authority-level)](/visas/[country-slug]/[visa-slug]/[authority-slug]/)
- [[COUNTRY_NAME] [VISA_TYPE_SHORT] visa hub](/visas/[country-slug]/[visa-slug]/)
- [Digital nomad insurance in [REGION]](/posts/digital-nomad-insurance-[region]/)
- [Methodology](/methodology/)

## Where to obtain compliant insurance for [COUNTRY_NAME] [VISA_TYPE_SHORT]

[AFFILIATE_BLOCK_PLACEHOLDER — Only include this section if at least one product shows GREEN for this route in the current snapshot. Copy the pattern from content/posts/portugal-dnv-insurance.md. Do not include if no GREEN mappings exist. Do not speculate about which products might pass — GREEN status must be confirmed in data/mappings/.]

{{< checker_cta visa="[VISA_ID]" snapshot="releases/2026-01-15" label="Check your insurance for [COUNTRY_NAME] [VISA_TYPE_SHORT]" >}}

*Affiliate disclosure: Links above are affiliate links.
We may earn a commission at no extra cost to you.
Compliance results are generated independently.
See [affiliate disclosure](/affiliate-disclosure/).*

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If a link is shown after results, it does not influence the evidence-based outcome.

Last updated: [YYYY-MM-DD]

## Evidence log

- Source: [SOURCE_ID]
```

---

## Template usage notes

1. **Affiliate discipline**: The "Where to obtain compliant insurance" section and any product links MUST be omitted if no product shows GREEN for the route in `data/mappings/`. Do not include a product link based on the assumption that it should pass — only include if the mapping file exists and shows GREEN.
2. **Banned words**: Certain words are prohibited in visafact.org content. Run the banned-word audit grep (documented in the expansion plan's Verification Strategy section) against the file before committing. Zero matches required.
3. **Snapshot value**: Every `{{< checker_cta >}}` call must include `snapshot="releases/2026-01-15"`. Update when a newer release snapshot is published.
4. **Five required sections**: The following headings must appear in the file (identical wording):
   - `## What the authority requires`
   - `## How we evaluate`
   - `## Check in the engine`
   - `## Disclaimer + Affiliate disclosure`
   - _(The "Where to obtain compliant insurance" section is conditional; the other four are not.)_
5. **Deep links with snapshot**: Any link to the checker UI that includes a `snapshot=` parameter must use `snapshot="releases/2026-01-15"` or a named release. Never use a floating snapshot reference.
6. **Evidence-based tone**: Use "the authority states", "the checklist requires", "evidence shows", "source confirms". Avoid "we think", "it seems", "likely passes".
7. **Publish order**: Publish the authority-level visa page (from `content_template_visa.md`) before publishing this post. The post's related-reading section links to the visa page; broken links at publish time harm the Hugo build.
