# Content Template — Authority-Level Visa Page

_Copy-paste this template to create a new `content/visas/<country>/<visa-type>/<authority>/index.md`. Replace all `[BRACKET]` placeholders before publishing. Do not publish until a `visa_facts.json` and at least one `data/mappings/*.json` file exist for this route._

---

```markdown
---
title: "[COUNTRY_NAME] [VISA_TYPE_FULL_NAME] - [AUTHORITY_FULL_NAME]"
visa_id: "[VISA_ID]"
last_verified: "[YYYY-MM-DD]"
source_ids: ["[SOURCE_ID]"]
description: "Official insurance requirements for [COUNTRY_NAME] [VISA_TYPE_FULL_NAME] via [AUTHORITY_FULL_NAME]."
faq:
  - question: "Is insurance mandatory for [VISA_ID_READABLE]?"
    answer: "[YES/NO]. [AUTHORITY_SHORT_NAME] [checklist/requirements page] lists [type of insurance] as a required document."
  - question: "Does the insurer have to be authorized in [COUNTRY_NAME]?"
    answer: "[YES/NO]. The [checklist/requirements page] [requires / does not require] insurance from an insurer authorized to operate in [COUNTRY_NAME]."
  - question: "Are deductibles or co-payments allowed?"
    answer: "[YES/NO/UNKNOWN]. [State exactly what the authority document says, or state UNKNOWN if not addressed.]"
  - question: "Is a minimum coverage amount required?"
    answer: "[YES/NO/UNKNOWN]. [State the amount if specified, e.g. ¥10,000,000 or €30,000; state UNKNOWN if not specified.]"
---

## Short answer

[COUNTRY_NAME] [VISA_TYPE_SHORT] ([AUTHORITY_SHORT_NAME] route) requires [one sentence stating the insurance requirement verbatim or closely paraphrased from the authority document]. (Source: `[SOURCE_ID]`, locator: [page/section reference]; verified [YYYY-MM-DD]).

## Key findings at a glance

| Item | Value |
|---|---|
| Route | [COUNTRY_NAME] [VISA_TYPE_SHORT] ([AUTHORITY_SHORT_NAME]) |
| Evidence verified | [YYYY-MM-DD] |
| Snapshot | releases/2026-01-15 |
| Core requirements | [comma-separated list of key requirements, e.g.: authorized insurer, ¥10M min coverage, Japan coverage explicit] |

## What the authority requires

- [Requirement 1]. (Source: `[SOURCE_ID]`, locator: [page/section]; verified [YYYY-MM-DD])
- [Requirement 2]. (Source: `[SOURCE_ID]`, locator: [page/section]; verified [YYYY-MM-DD])
- [Add one bullet per distinct requirement; do not combine requirements into one bullet]

Normalized requirements table:

| Requirement | Source URL | Locator | Verified date |
|---|---|---|---|
| [Requirement 1 short label] | [authority_source_url] | [page/section] | [YYYY-MM-DD] |
| [Requirement 2 short label] | [authority_source_url] | [page/section] | [YYYY-MM-DD] |

## Verified requirements (PASS/FAIL/UNKNOWN)

| Requirement | Status | Evidence |
|---|---|---|
| [Requirement 1] | PASS | [SOURCE_ID], [locator] |
| [Requirement 2] | PASS | [SOURCE_ID], [locator] |
| [Optional requirement not in source] | UNKNOWN | Not stated in [SOURCE_ID] |

## How we evaluate

The checker compares each requirement to product evidence. If a requirement is explicitly contradicted (for example, a deductible where none is allowed), the result is RED. If evidence is missing, the result is UNKNOWN rather than inferred. See /methodology/ for rule logic and the UNKNOWN > Wrong principle.

## Proof package checklist

- [Document 1 the applicant must provide, e.g.: Policy certificate confirming minimum [AMOUNT] coverage.]
- [Document 2, e.g.: Documentation that the insurer is authorized to operate in [COUNTRY_NAME].]
- [Document 3 if applicable]

## Common rejection traps

- [Trap 1 — state what the authority forbids and what documents get rejected. Do not invent traps; only include what evidence supports.]
- [Trap 2]
- INFERENCE: [Any inferred trap must be explicitly labelled INFERENCE.]

## FAQ

**Q: [Question from front matter 1]**
**A:** [Answer from front matter 1] (Source: `[SOURCE_ID]`, [locator]; verified [YYYY-MM-DD]).

**Q: [Question from front matter 2]**
**A:** [Answer from front matter 2] (Source: `[SOURCE_ID]`, [locator]; verified [YYYY-MM-DD]).

**Q: [Question from front matter 3]**
**A:** [Answer from front matter 3]

**Q: [Question from front matter 4]**
**A:** [Answer from front matter 4]

## Check in the engine

Use [the compliance checker](/ui/) with the current snapshot for this route:

{{< checker_cta visa="[VISA_ID]" snapshot="releases/2026-01-15" >}}

## Mapping results summary

As of snapshot `releases/2026-01-15`, the checker evaluated [N] products:

| Status | Count | What it means |
|---|---|---|
| GREEN | [N] | Evidence matches all requirements |
| RED | [N] | Evidence conflicts with one or more requirements |
| UNKNOWN | [N] | Evidence missing for at least one requirement |

[If no mappings exist yet, write: "Mapping data for this route has not yet been published. Check back after the next data release."]

## Related reading

- [[COUNTRY_NAME] [VISA_TYPE_SHORT] insurance hub](/posts/[country-slug]-[visa-slug]-insurance/)
- [[COUNTRY_NAME] [VISA_TYPE_SHORT] visa hub](/visas/[country-slug]/[visa-slug]/)
- [How to read compliance results](/guides/how-to-read-results/)
- [Methodology](/methodology/)

## Disclaimer + Affiliate disclosure

Not legal advice. Compliance results are evidence-based snapshots.

If an affiliate link is present, it appears only after results and does not change the compliance outcome.

Last updated: [YYYY-MM-DD]

## Evidence log

- Source: [SOURCE_ID]
```

---

## Template usage notes

1. **Banned words**: Certain words are prohibited in visafact.org content. Run the banned-word audit grep (documented in the expansion plan's Verification Strategy section) against the file before committing. Zero matches required.
2. **Snapshot value**: Every `{{< checker_cta >}}` call must include `snapshot="releases/2026-01-15"`. Update when a newer release snapshot is published.
3. **Evidence-based tone**: Use "the authority states", "evidence shows", "source confirms", "the checklist requires" — not "you should" or "we think".
4. **UNKNOWN vs inferred**: If a requirement is not stated in the source, mark it UNKNOWN in the verified table. Do not infer a PASS from absence.
5. **FAQ minimum**: Include exactly 4 FAQ items in the front matter matching the 4 FAQ sections in the body.
6. **Required sections**: The five sections required by lint rules must appear with these exact heading strings:
   - `## What the authority requires`
   - `## How we evaluate`
   - `## Check in the engine`
   - `## Disclaimer + Affiliate disclosure`
   - _(Affiliate disclosure is embedded in the Disclaimer section heading above; the checker shortcode heading "Check in the engine" doubles as the engine section)_
7. **Affiliate links**: Only include a product link in the Mapping results summary if that product is GREEN in the named snapshot. The affiliate block pattern from `content/posts/portugal-dnv-insurance.md` is the canonical reference.
