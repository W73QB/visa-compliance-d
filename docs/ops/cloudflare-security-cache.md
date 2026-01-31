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
Remove legacy cache rules before enabling Cache Everything.

1) Remove legacy rules (if present)
- Bypass HTML
- Bypass ui_index.json
- Asset-only caching rules

2) Cache Everything (hostname-wide)
- If Hostname equals `visafact.org` -> Cache Everything
- Edge TTL: 24 hours
- Browser TTL: 1 hour

3) Purge on deploy
- GitHub Actions runs a Cloudflare purge after deploy (see `.github/workflows/pages.yml`).
  This prevents stale HTML after each release.

## Manual verification
- `curl -I https://visafact.org/ui/` includes the security headers above.
- `curl -I https://visafact.org/` shows `cf-cache-status: HIT` on the second request.
- `curl -I https://visafact.org/posts/digital-nomad-insurance-europe/` shows `cf-cache-status: HIT` on the second request.
