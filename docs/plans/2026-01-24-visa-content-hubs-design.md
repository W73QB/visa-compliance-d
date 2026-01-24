# Visa Content Hubs Design

**Goal:** Create scalable, evidence-first content hubs for all visa routes to grow SEO traffic and funnel users to the checker without compromising data integrity.

## Scope
- Create a new Hugo section at `content/visas/`.
- Generate hubs from existing data (`data/visas/**/visa_facts.json` and `sources/*.meta.json`).
- Provide hub overview pages and route-specific pages with evidence links.
- Keep content aligned with evidence; do not introduce new requirements without sources.

## Non-Goals
- No new visa requirements or product claims without evidence.
- No changes to engine logic or mapping rules.
- No price estimates inside ProductFacts.

## URL Strategy
- Hub overview: `/visas/<country>/<visa>/`  
  Example: `/visas/spain/dnv/`
- Route detail: `/visas/<country>/<visa>/<authority>/`  
  Example: `/visas/spain/dnv/bls-london/`

No redirects from overview to route detail. Each page is canonical to itself.

## Content Model
### Hub Overview Page
- Summary: what the visa route is.
- Evidence-first note: all requirements come from official sources.
- Route table:
  - Authority/route name
  - Last verified date
  - Link to route detail page
- CTA: link to `/ui/` with context text.

### Route Detail Page
- Header: country, visa name, authority/route.
- Requirements table:
  - Requirement key
  - Operator/value
  - Evidence excerpt
  - Source link (local snapshot)
- Metadata: last_verified, source_id list.
- CTA to checker.

## Data Flow
1. Read all `visa_facts.json`.
2. Normalize country/visa/authority slugs for URLs.
3. Build route detail pages from each visa_facts entry.
4. Build hub overview pages by grouping routes by (country, visa).
5. Use source meta data to build evidence links to `static/sources/`.

## Generation Approach
Create a script (example: `tools/build_content_hubs.py`) that writes markdown files:
- `content/visas/<country>/<visa>/_index.md` (overview)
- `content/visas/<country>/<visa>/<authority>/index.md` (detail)

Use Hugo shortcodes (`vf-cta`) for consistent CTA styling.

## SEO Considerations
- Use descriptive titles and meta descriptions.
- Add breadcrumb structure through Hugo templates if available.
- FAQPage schema only when FAQ is visible on the page.
- Avoid duplicate content by keeping overview pages summary-only.

## Accessibility
- Use semantic HTML in templates (headers, tables, lists).
- Ensure keyboard navigation and focus styles in CSS.
- Avoid dense tables without row headers.

## Testing
Add PowerShell tests to verify:
- Overview and route pages exist for each visa_facts entry.
- Route pages include at least one evidence link.
- Overview pages list all routes for their group.

## Rollout Order
1. Spain DNV
2. Portugal D8
3. Germany Freelance
4. Thailand DTV
5. Malta Nomad
6. Costa Rica DN

## Risks and Mitigations
- **Risk:** Content drift from data.  
  **Mitigation:** Generate pages from source data only.
- **Risk:** Duplicate content.  
  **Mitigation:** Keep overview short; route detail carries evidence.
- **Risk:** Broken source links.  
  **Mitigation:** Link to local snapshots in `static/sources/`.

