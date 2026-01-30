# Evidence Density Standard

## Minimum Requirements per Content Type

### Hub Post (content/posts/)
- >= 3 evidence items cited (source_id references)
- >= 1 government/consulate source
- >= 1 product_facts reference
- All claims link to snapshot= deep links

### Visa Route Page (content/visas/**/index.md)
- Generated from visa_facts.json
- Gate (Option B): Route passes if (a) >= 2 requirements with evidence OR (b) insurance_not_required = true OR (c) exactly 1 requirement with evidence from a primary source
- Each requirement must have source_id + locator

### Trap Page (content/traps/)
- >= 2 evidence items showing the trap scenario
- >= 1 mapping result demonstrating the issue

### Guide Page (content/guides/)
- >= 2 evidence items
- Step-by-step must reference actual tool output

### Comparison Page
- >= 1 evidence item per product compared
- All product claims from product_facts.json
