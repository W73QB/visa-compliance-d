## 2026-02-08 - Vanilla JS Modal Accessibility
**Learning:** Modals in this project are implemented with vanilla JS and Tailwind, lacking native `dialog` element features. They require manual implementation of ARIA attributes (`role="dialog"`, `aria-modal`, `aria-labelledby`) and keyboard handlers (Escape key, focus management).
**Action:** When touching modals, always ensure `role="dialog"`, `aria-modal="true"`, and an Escape key listener are present.

## 2026-02-08 - Form Label Association
**Learning:** Native `<select>` elements in the main UI were not associated with their visual labels using `for` attributes, breaking screen reader navigation.
**Action:** Always check `for` attributes on labels when modifying forms in `ui/index.html`.
