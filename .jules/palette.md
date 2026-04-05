## 2026-02-01 - Vanilla JS Modal Accessibility
**Learning:** The project uses a single HTML file with vanilla JS for UI. Modals are implemented manually without a library, requiring explicit implementation of accessibility features like `role="dialog"`, `aria-modal="true"`, focus trapping, and Escape key handling.
**Action:** When modifying or adding interactive components in `ui/index.html`, always manually verify and implement keyboard accessibility and ARIA attributes, as there is no framework to handle this automatically. Use Playwright for verification as existing tests are static.
