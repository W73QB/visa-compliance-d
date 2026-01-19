## 2024-05-22 - Modal Accessibility & File Encoding
**Learning:** Modals in this codebase require manual focus management (save/restore active element) and explicit ARIA attributes (`role="dialog"`, `aria-modal="true"`). The `ui/index.html` file requires BOM (`utf-8-sig`) and CRLF line endings to work correctly with the build tools and diffs.
**Action:** When editing `ui/index.html`, preserve BOM/CRLF and ensure all overlays manage focus and attributes explicitly. Verify using Playwright.
