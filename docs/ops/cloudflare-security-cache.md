# Cloudflare Security Headers and Cache Rules

## Purpose
Define the required response headers and cache rules for the GitHub Pages origin behind Cloudflare.

## Security headers (Rules > Transform Rules > Modify Response Header)
Apply to all responses:

```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; base-uri 'self'; frame-ancestors 'none'; object-src 'none'
```

Notes:
- `script-src` includes 'unsafe-inline' because ui/index.html uses inline scripts and an onclick handler.
- If inline scripts are moved to external files, remove 'unsafe-inline' and tighten CSP.

## Cache rules (Rules > Cache Rules)
Order matters. Put bypass rules above cache rules.

1) Bypass HTML
- If URI Path ends with `.html` -> Bypass cache

2) Bypass ui_index.json
- If URI Path ends with `/ui_index.json` -> Bypass cache

3) Cache assets
- If URI Path ends with `.css` -> Cache 4 hours
- If URI Path ends with `.js` -> Cache 4 hours
- If URI Path ends with `.woff2` -> Cache 1 year
- If URI Path ends with `.png` or `.jpg` or `.svg` -> Cache 1 year

## Manual verification
- `curl -I https://visafact.org/ui/` includes the security headers above.
- `curl -I https://visafact.org/data/ui_index.json` shows `cf-cache-status: BYPASS`.
- `curl -I https://visafact.org/ui/style.css` shows `cf-cache-status: HIT` or `MISS` with a cache TTL.
