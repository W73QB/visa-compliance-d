# SEO Content Growth (Hybrid) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve organic traffic by fixing thin content and missing internal links, while leveraging existing FAQ schema and evidence-based positioning.

**Architecture:** Add a lightweight SEO audit script + test to enforce baseline content/linking rules. Expand a small set of high-impact posts manually, and automate internal linking for visa pages via the existing content generator. Keep changes scoped to content + generator + tests (no monetization/ads in this phase).

**Tech Stack:** Hugo (PaperMod), Markdown content, Python tools, PowerShell tests.

---

### Task 0: Create isolated worktree (correct sequence)

**Files:**
- Create: none
- Modify: none
- Test: none

**Step 1: Create branch (without checking it out)**

Run:
```bash
git branch feat/seo-content-growth-hybrid
```
Expected: branch created.

**Step 2: Create worktree for the branch**

Run:
```bash
git worktree add .worktrees/seo-content-growth-hybrid feat/seo-content-growth-hybrid
```
Expected: worktree created at `.worktrees/seo-content-growth-hybrid`.

**Step 3: Move into worktree and check branch**

Run:
```bash
cd .worktrees/seo-content-growth-hybrid
```
Expected: all edits below occur in this worktree.

---

### Task 1: Add SEO audit tool + tests (baseline guardrails)

**Files:**
- Create: `tools/seo_audit.py`
- Create: `tools/seo_thresholds.json`
- Create: `tools/tests/seo_audit_tests.ps1`

**Step 1: Write failing test**

Create `tools/tests/seo_audit_tests.ps1`:
```powershell
$ErrorActionPreference = "Stop"
$root = (Resolve-Path "$PSScriptRoot/../..").Path

$proc = Start-Process -FilePath "py" -ArgumentList "tools/seo_audit.py --config tools/seo_thresholds.json" -WorkingDirectory $root -Wait -PassThru -NoNewWindow

if ($proc.ExitCode -ne 0) {
  throw "seo_audit failed (expected to fail before content updates)"
}
```
Expected: FAIL because `tools/seo_audit.py` does not exist yet.

**Step 2: Run test to verify it fails**

Run:
```bash
pwsh -File tools/tests/seo_audit_tests.ps1
```
Expected: FAIL with message `seo_audit failed...`.

**Step 3: Create thresholds config (phase 1 targets)**

Create `tools/seo_thresholds.json`:
```json
{
  "min_word_count": {
    "default": 150,
    "content/posts/spain-dnv-insurance.md": 300,
    "content/posts/germany-freelance-insurance.md": 250,
    "content/posts/portugal-dnv-insurance.md": 250,
    "content/posts/thailand-dtv-insurance.md": 200,
    "content/posts/safetywing-vs-worldnomads-vs-genki.md": 350,
    "content/posts/digital-nomad-insurance-europe.md": 350,
    "content/posts/digital-nomad-insurance-asia.md": 250,
    "content/posts/digital-nomad-insurance-americas.md": 250,
    "content/posts/costa-rica-dn-insurance.md": 225,
    "content/guides/how-to-read-results.md": 150
  },
  "required_links": [
    {
      "glob": "content/posts/*.md",
      "must_include": ["/ui/"],
      "at_least_one_of": ["/visas/"]
    },
    {
      "glob": "content/visas/**/index.md",
      "must_include": ["/ui/"],
      "at_least_one_of": ["/posts/"]
    }
  ],
  "include_globs": [
    "content/posts/*.md",
    "content/guides/*.md",
    "content/traps/*.md",
    "content/visas/**/index.md"
  ],
  "exclude_globs": [
    "content/posts/_index.md",
    "content/posts/hello.md",
    "content/templates/*.md",
    "content/legal/**"
  ],
  "require_faq": [
    "content/posts/spain-dnv-insurance.md",
    "content/posts/germany-freelance-insurance.md",
    "content/posts/portugal-dnv-insurance.md",
    "content/posts/thailand-dtv-insurance.md",
    "content/posts/safetywing-vs-worldnomads-vs-genki.md",
    "content/guides/schengen-30000-insurance.md",
    "content/guides/how-to-read-results.md",
    "content/traps/spain-dnv-insurance-mistakes.md",
    "content/traps/malta-nomad-monthly-payments.md",
    "content/posts/costa-rica-dn-insurance.md"
  ]
}
```

**Step 4: Implement audit script**

Create `tools/seo_audit.py`:
```python
#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from fnmatch import fnmatch

ROOT = Path(__file__).parent.parent

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def split_frontmatter(text: str):
    text = text.lstrip("\ufeff")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text

def has_frontmatter_key(fm: str, key: str) -> bool:
    return re.search(rf"^{re.escape(key)}\s*:", fm, re.M) is not None

def word_count(body: str) -> int:
    body = re.sub(r"[`*_>#\\[\\]()-]", " ", body)
    words = re.findall(r"\b\w+\b", body)
    return len(words)

def link_matches(body: str, token: str) -> bool:
    return token in body

def load_thresholds(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def iter_markdown():
    for p in ROOT.glob("content/**/*.md"):
        yield p

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_thresholds(ROOT / args.config)
    min_word_count = cfg.get("min_word_count", {})
    required_links = cfg.get("required_links", [])
    require_faq = set(cfg.get("require_faq", []))

    failures = []

    for path in iter_markdown():
        rel = str(path.relative_to(ROOT))
        text = read_file(path)
        fm, body = split_frontmatter(text)
        wc = word_count(body)

        target_wc = min_word_count.get(rel, min_word_count.get("default", 0))
        if wc < target_wc:
            failures.append(f"{rel}: word_count {wc} < {target_wc}")

        if rel in require_faq and not has_frontmatter_key(fm, "faq"):
            failures.append(f"{rel}: missing faq frontmatter")

        for rule in required_links:
            if fnmatch(rel, rule.get("glob", "")):
                for must in rule.get("must_include", []):
                    if not link_matches(body, must):
                        failures.append(f"{rel}: missing required link {must}")
                any_of = rule.get("at_least_one_of", [])
                if any_of and not any(link_matches(body, tok) for tok in any_of):
                    failures.append(f"{rel}: missing any of {any_of}")

    if failures:
        print("SEO audit failures:")
        for f in failures:
            print(f" - {f}")
        raise SystemExit(1)

    print("SEO audit passed.")

if __name__ == "__main__":
    main()
```

**Step 5: Run test to verify it now passes (expected to still FAIL until content updates)**

Run:
```bash
pwsh -File tools/tests/seo_audit_tests.ps1
```
Expected: FAIL due to content not yet updated.

**Step 6: Commit**

```bash
git add tools/seo_audit.py tools/seo_thresholds.json tools/tests/seo_audit_tests.ps1
git commit -m "test: add SEO audit guardrails"
```

---

### Task 2: Add related-reading links to visa pages (generator update)

**Files:**
- Modify: `tools/build_content_hubs.py`
- Modify: `content/visas/**/index.md` (regenerated)
- Test: `tools/tests/seo_audit_tests.ps1`, `tools/tests/visa_hubs_tests.ps1`

**Step 1: Write failing test**

Update `tools/seo_thresholds.json` rule already requires visa pages to include at least one `/posts/` link.  
This will remain FAIL until generator is updated and content regenerated.

**Step 2: Implement related-reading mapping**

In `tools/build_content_hubs.py`, add near top (after constants):
```python
RELATED_POSTS = {
    "ES_DNV_BLS_LONDON_2026": [
        ("/posts/spain-dnv-insurance/", "Spain DNV insurance requirements"),
        ("/posts/safetywing-spain-dnv-rejected/", "Why SafetyWing gets rejected for Spain DNV"),
        ("/traps/spain-dnv-insurance-mistakes/", "Spain DNV insurance mistakes to avoid")
    ],
    "DE_FREELANCE_EMBASSY_LONDON_2026": [
        ("/posts/germany-freelance-insurance/", "Germany freelance visa insurance guide"),
        ("/guides/how-to-read-results/", "How to read compliance results")
    ],
    "PT_DNV_VFS_CHINA_2026": [
        ("/posts/portugal-dnv-insurance/", "Portugal DNV insurance requirements"),
        ("/guides/schengen-30000-insurance/", "Schengen 30,000 EUR insurance rule")
    ],
    "CR_DN_DECREE_43619_2026": [
        ("/posts/costa-rica-dn-insurance/", "Costa Rica DN insurance requirements"),
        ("/guides/how-to-read-results/", "How to read compliance results")
    ],
    "TH_DTV_MFA_2026": [
        ("/posts/thailand-dtv-insurance/", "Thailand DTV insurance overview"),
        ("/posts/digital-nomad-insurance-asia/", "Digital nomad insurance in Asia")
    ],
    "MT_NOMAD_RESIDENCY_2026": [
        ("/posts/malta-nomad-insurance/", "Malta nomad insurance requirements"),
        ("/traps/malta-nomad-monthly-payments/", "Monthly payment pitfalls for Malta nomad visa")
    ]
}
```

**Step 3: Render related-reading section**

In `render_detail`, before lint blocks, add:
```python
    related = RELATED_POSTS.get(visa_id, [])
    if related:
        lines.append("")
        lines.append("## Related reading")
        lines.append("")
        for url, label in related:
            lines.append(f"- [{label}]({url})")
```

**Step 4: Regenerate visa content**

Run:
```bash
py tools/build_content_hubs.py
```
Expected: `content/visas/**/index.md` regenerated.

**Step 5: Run tests**

Run:
```bash
pwsh -File tools/tests/visa_hubs_tests.ps1
pwsh -File tools/tests/seo_audit_tests.ps1
```
Expected: visa hubs test PASS; SEO audit may still FAIL until posts are updated.

**Step 6: Commit**

```bash
git add tools/build_content_hubs.py content/visas
git commit -m "feat: add related-reading links to visa hubs"
```

---

### Task 3: Expand high-impact posts + add internal links and FAQ

**Files:**
- Modify: `content/posts/spain-dnv-insurance.md`
- Modify: `content/posts/germany-freelance-insurance.md`
- Modify: `content/posts/portugal-dnv-insurance.md`
- Modify: `content/posts/thailand-dtv-insurance.md`
- Modify: `content/posts/safetywing-vs-worldnomads-vs-genki.md`

**Step 1: Update Spain DNV post (append only)**

Note: `content/posts/spain-dnv-insurance.md` already has a `faq:` block. Do **not** add a second `faq:` block.

Append after "Check in the engine" section:
```markdown
## Plain-English summary

Spain DNV authorities ask for **comprehensive, Spain-authorized health insurance** that mirrors the public system. If any requirement lacks official evidence, the checker returns **UNKNOWN** instead of guessing.

## Common pitfalls

- Buying travel-only policies when a health policy is required.
- Accepting deductibles or co-payments when the route requires zero.
- Paying monthly when a full annual policy is expected.

## Related reading

- [Spain DNV requirements (route page)](/visas/spain/digital-nomad-visa/consulate-via-bls-london/)
- [Spain DNV insurance mistakes](/traps/spain-dnv-insurance-mistakes/)
- [Why SafetyWing is rejected for Spain DNV](/posts/safetywing-spain-dnv-rejected/)
```

**Step 2: Update Germany Freelance post (append only)**

Note: `content/posts/germany-freelance-insurance.md` already has a `faq:` block. Do **not** add a second `faq:` block.

Append:
```markdown
## Plain-English summary

Germany freelance routes often expect health coverage that matches long-stay requirements. The checker uses evidence snapshots so you can see which requirements are verified.

## Common pitfalls

- Submitting travel policies where long-stay health coverage is required.
- Assuming a provider is accepted without route-specific evidence.

## Related reading

- [Germany freelance visa requirements (route page)](/visas/germany/freelance-visa-national-d/embassy-london/)
- [How to read compliance results](/guides/how-to-read-results/)
```

**Step 3: Update Portugal DNV post**

Add FAQ frontmatter (only if missing):
```yaml
faq:
  - question: "Which authority sets Portugal DNV insurance rules?"
    answer: "The route authority (e.g., VFS/consulate) defines the checklist. Evidence varies by route."
  - question: "Is Schengen coverage relevant?"
    answer: "Some routes align with Schengen limits; use the checker for verified requirements."
```

Append:
```markdown
## Plain-English summary

Portugal DNV routes can differ by authority. This page summarizes the verified requirements and points you to evidence excerpts.

## Common pitfalls

- Using a policy with missing evidence for a required feature.
- Relying on generic insurance advice instead of route-specific rules.

## Related reading

- [Portugal DNV requirements (route page)](/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/)
- [Schengen 30,000 EUR insurance rule](/guides/schengen-30000-insurance/)
```

**Step 4: Update Thailand DTV post**

Add FAQ frontmatter (only if missing):
```yaml
faq:
  - question: "Is insurance mandatory for Thailand DTV?"
    answer: "Some routes list insurance as optional or not required. Use the checker for route evidence."
  - question: "Should I still carry insurance?"
    answer: "Even when not mandatory, coverage can protect against unexpected medical costs."
```

Append:
```markdown
## Plain-English summary

Thailand DTV routes may not mandate insurance, but requirements can change. VisaFact highlights evidence so you can see what is verified vs unknown.

## Common pitfalls

- Assuming “not required” means no proof will ever be requested.
- Using a policy with unclear coverage or missing evidence.

## Related reading

- [Thailand DTV requirements (route page)](/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/)
- [Digital nomad insurance in Asia](/posts/digital-nomad-insurance-asia/)
```

**Step 5: Update comparison post**

Add FAQ frontmatter (only if missing):
```yaml
faq:
  - question: "Which insurer is most likely to pass visa checks?"
    answer: "It depends on the route. Use the checker to compare compliance against official evidence."
  - question: "Why do some products show UNKNOWN?"
    answer: "UNKNOWN means we found no official evidence for a requirement."
```

Replace the intro with:
```markdown
This comparison focuses on **evidence-based compliance**, not marketing claims. If evidence is missing, we show **UNKNOWN** rather than guessing.
```

Append:
```markdown
## How to interpret this comparison

Compliance depends on the visa authority and route. Use the checker links below to see evidence for each product and route.

## Quick chooser

- If a route requires **no deductibles**, avoid products with fixed deductibles.
- If a route requires **authorized local insurers**, prioritize products with evidence of authorization.
- If requirements are unclear, prefer products with documented evidence and use the checker to validate.

## Related reading

- [Spain DNV requirements](/posts/spain-dnv-insurance/)
- [Germany freelance visa insurance](/posts/germany-freelance-insurance/)
- [Portugal DNV insurance](/posts/portugal-dnv-insurance/)
```

**Step 6: Run audit test (expected may still FAIL until regional posts updated)**

Run:
```bash
pwsh -File tools/tests/seo_audit_tests.ps1
```

**Step 7: Commit**

```bash
git add content/posts/spain-dnv-insurance.md content/posts/germany-freelance-insurance.md content/posts/portugal-dnv-insurance.md content/posts/thailand-dtv-insurance.md content/posts/safetywing-vs-worldnomads-vs-genki.md
git commit -m "docs: expand core visa and comparison posts"
```

---

### Task 4: Expand regional hub posts (Europe/Asia/Americas) + internal links

**Files:**
- Modify: `content/posts/digital-nomad-insurance-europe.md`
- Modify: `content/posts/digital-nomad-insurance-asia.md`
- Modify: `content/posts/digital-nomad-insurance-americas.md`

**Step 1: Add intro and internal links**

Append to each file (adjust region names and links):

`content/posts/digital-nomad-insurance-europe.md`:
```markdown
## Countries covered in this hub

- [Spain DNV requirements](/visas/spain/digital-nomad-visa/consulate-via-bls-london/)
- [Portugal DNV requirements](/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/)
- [Germany freelance visa requirements](/visas/germany/freelance-visa-national-d/embassy-london/)
- [Malta nomad residence permit requirements](/visas/malta/nomad-residence-permit/residency-malta-agency/)

## Use the compliance checker

Try the evidence-based checker for your route: /ui/
```

`content/posts/digital-nomad-insurance-asia.md`:
```markdown
## Countries covered in this hub

- [Thailand DTV requirements](/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/)

## Use the compliance checker

Try the evidence-based checker for your route: /ui/
```

`content/posts/digital-nomad-insurance-americas.md`:
```markdown
## Countries covered in this hub

- [Costa Rica digital nomad visa requirements](/visas/costa-rica/digital-nomad-visa/executive-decree-43619/)

## Use the compliance checker

Try the evidence-based checker for your route: /ui/
```

**Step 2: Run audit test**

Run:
```bash
pwsh -File tools/tests/seo_audit_tests.ps1
```
Expected: PASS if thresholds and links are satisfied.

**Step 3: Commit**

```bash
git add content/posts/digital-nomad-insurance-europe.md content/posts/digital-nomad-insurance-asia.md content/posts/digital-nomad-insurance-americas.md
git commit -m "docs: expand regional insurance hubs with internal links"
```

---

### Task 5: Add FAQ blocks to guides and traps

**Files:**
- Modify: `content/guides/how-to-read-results.md`
- Modify: `content/guides/schengen-30000-insurance.md`
- Modify: `content/traps/spain-dnv-insurance-mistakes.md`
- Modify: `content/traps/malta-nomad-monthly-payments.md`
 - Modify: `content/posts/costa-rica-dn-insurance.md`

**Step 1: Add FAQ frontmatter**

Add to each file:

`content/guides/how-to-read-results.md`:
```yaml
faq:
  - question: "What does UNKNOWN mean?"
    answer: "UNKNOWN means we found no official evidence for a requirement."
  - question: "Is GREEN a guarantee?"
    answer: "No. GREEN means evidence matches requirements, not a visa approval guarantee."
```

`content/guides/schengen-30000-insurance.md`:
```yaml
faq:
  - question: "Is 30,000 EUR always required?"
    answer: "Many Schengen routes require it, but verify with the authority checklist."
  - question: "Does deductible matter?"
    answer: "Some routes require zero deductible. Use the checker for evidence."
```

`content/traps/spain-dnv-insurance-mistakes.md`:
```yaml
faq:
  - question: "What is the most common rejection reason?"
    answer: "Submitting travel insurance instead of comprehensive health coverage."
  - question: "Can monthly plans be rejected?"
    answer: "Some routes expect annual prepaid coverage."
```

`content/traps/malta-nomad-monthly-payments.md`:
```yaml
faq:
  - question: "Are monthly plans accepted for Malta nomad permit?"
    answer: "Evidence indicates monthly payments are not accepted for some routes."
  - question: "How can I verify acceptance?"
    answer: "Use the checker and review evidence excerpts."
```

`content/posts/costa-rica-dn-insurance.md` (if missing):
```yaml
faq:
  - question: "What is the minimum coverage for Costa Rica DN visa?"
    answer: "Evidence indicates a $50,000 minimum coverage requirement for medical expenses."
  - question: "How do I verify if a policy is compliant?"
    answer: "Use the checker to compare evidence-backed requirements against product facts."
```

**Step 2: Run audit test**

Run:
```bash
pwsh -File tools/tests/seo_audit_tests.ps1
```
Expected: PASS.

**Step 3: Commit**

```bash
git add content/guides/how-to-read-results.md content/guides/schengen-30000-insurance.md content/traps/spain-dnv-insurance-mistakes.md content/traps/malta-nomad-monthly-payments.md content/posts/costa-rica-dn-insurance.md
git commit -m "docs: add FAQ blocks to guides and traps"
```

---

### Task 6: Full verification (align with CI)

**Files:**
- Test: `tools/tests/*.ps1`

**Step 1: Run key build steps**

```bash
py tools/validate.py
py tools/build_mappings.py
py tools/build_index.py
py tools/build_content_hubs.py
py tools/sync_hugo_static.py
```
Expected: no errors.

**Step 2: Enable SEO audit in CI (after content passes)**

Modify `.github/workflows/pages.yml` to add after existing tests:
```yaml
      - name: SEO audit tests
        run: pwsh -File tools/tests/seo_audit_tests.ps1
```

**Step 3: Run tests**

```bash
pwsh -File tools/tests/content_lint_tests.ps1
pwsh -File tools/tests/visa_hubs_tests.ps1
pwsh -File tools/tests/seo_audit_tests.ps1
pwsh -File tools/tests/ui_compliance_tests.ps1
pwsh -File tools/tests/schema_tests.ps1
```
Expected: all PASS.

**Step 4: Commit final changes if any**

```bash
git status -s
```
Expected: clean.

---

## Definition of Done

- `tools/seo_audit.py` exists and passes with updated content.
- Visa hub pages include **Related reading** linking to `/posts/`.
- Target posts meet minimum word counts and include FAQ + internal links.
- Regional hub posts link to visa routes and `/ui/`.
- CI includes SEO audit test and passes locally.

---

**Plan complete and saved to `docs/plans/2026-01-26-seo-content-growth-hybrid.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration  
**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
