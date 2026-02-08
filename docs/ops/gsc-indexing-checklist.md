# GSC Indexing Sanity Checklist

## Prereqs
- Access to Google Search Console property for https://visafact.org/

## Fast checks (10 minutes)
- Confirm https://visafact.org/robots.txt is reachable and does not block key paths.
- Confirm sitemap is reachable and submitted in GSC.
- In GSC, check "Pages" report for spikes in Not indexed / Crawled - currently not indexed.
- In GSC, check "Enhancements" for breadcrumb or unparsable structured data issues; treat these as rich-result blockers first, then validate indexing separately via URL Inspection.

## URL inspection (per key page)
Run for each:
- https://visafact.org/
- https://visafact.org/ui/
- https://visafact.org/posts/spain-dnv-insurance/
- One visa detail page under /visas/

Checklist:
- URL is on Google (or "Request indexing" used after deploy).
- Crawled page is the expected canonical (no unexpected redirects).
- "Indexing allowed" is true (no noindex).
- Fetch state is OK and resources load.

## Internal consistency checks
- Canonical points to the same final URL (no mixed http/https, no trailing mismatch).
- Pages that are intentionally gated use robots noindex (for example programmatic pages with no evidence).
- The UI page is allowed if it is intended to rank; otherwise ensure it is consistently noindex.

## Post-change monitoring (48 hours)
- Re-check GSC "Pages" and "Sitemaps" for new errors.
- Spot-check top landing pages for unexpected deindexing.
