## 2024-05-22 - XSS in Dynamic Links
**Vulnerability:** Unsanitized user/data input was being inserted directly into `href` attributes in `ui/index.html`. This allowed for `javascript:` protocol injection and HTML attribute injection via `innerHTML`.
**Learning:** `escapeHtml` is insufficient for `href` attributes because it doesn't prevent `javascript:` execution. Direct DOM property assignment (`.href = ...`) prevents attribute injection but not protocol injection.
**Prevention:** Always sanitize URLs to a safe allowlist (http, https, etc.) and use `escapeHtml` when inserting into HTML strings. Used a `sanitizeUrl` helper function.
