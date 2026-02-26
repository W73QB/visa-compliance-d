## 2026-02-26 - Accessibility in Custom Modals and Flex Forms

**Learning:**
1.  **Flex-col Form Layouts:** When using `flex-col` to stack labels and inputs, developers often omit the `for` attribute because visual proximity feels sufficient. However, this breaks accessibility for screen readers and reduces the click target area for mouse users. Explicitly linking `<label for="id">` to `<input id="id">` is critical even in modern frameworks.
2.  **Modal Focus Management:** A simple custom modal implementation (toggling a `hidden` class) is insufficient for accessibility. Adding `role="dialog"`, `aria-modal="true"`, trapping focus (or at least managing focus entry/exit), and supporting the `Escape` key are essential for keyboard users. These can be implemented with vanilla JS in < 20 lines without external libraries.
3.  **Tailwind Visibility:** Reliance on utility classes like `hidden` requires the CSS build step to be active. Verification tools (like Playwright) checking for visibility will fail if the CSS is missing, even if the class is present on the element.

**Action:**
- Always verify form labels have `for` attributes matching input `id`s, especially in `flex` layouts.
- When implementing or reviewing custom modals, ensure `Escape` key support and focus restoration logic are present.
- Ensure `pnpm build:css` is part of the verification pipeline for UI visibility checks.
