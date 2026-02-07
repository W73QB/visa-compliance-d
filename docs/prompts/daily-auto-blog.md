# Daily Auto Blog Prompt Contract

Base writing contract: `docs/prompts/writing-vi.md`

Output must be a Hugo markdown post with valid YAML front matter and all SOP blocks.

Front matter required keys:
- `title`
- `date`
- `description`
- `tags`
- `faq` with `question` and `answer`

Body must include all 11 SOP blocks from `docs/sop/content-workflow.md`:
1. Short answer
2. Key findings at a glance
3. What the authority requires
4. Verified requirements
5. How we evaluate
6. Proof package checklist
7. Common rejection traps
8. FAQ
9. Check in the engine
10. Disclaimer + Affiliate disclosure
11. Evidence log

Hard requirements:
- Use Hugo shortcode deep link format: `{{< checker_cta visa="..." snapshot="releases/{run_date}" >}}`.
- No unsourced factual claims. If source is missing, mark `UNKNOWN`.
- Avoid banned words from `tools/lint_content.py` (`best`, `recommend`, `recommended`, `guarantee`, `guaranteed`, `100%`, `approved`, `surely`).
- Front matter MUST validate against `tools/schemas/daily_front_matter.schema.json`.
- Output format must be flat file post (`content/posts/{slug}.md`).
- Slug convention: `{country}-{visa_type}-{topic_slug}`.
- FAQ block style must use bold pairs: `**Q: ...**` then `**A:** ...`.
- Each FAQ answer must include a source reference or explicit `UNKNOWN`.
