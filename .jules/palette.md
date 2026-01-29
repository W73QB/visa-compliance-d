## 2026-01-29 - Modal Accessibility Pattern
**Learning:** Vanilla JS modals (div-based) require explicit management of focus (trap within modal, restore to trigger, set initial focus) and ARIA attributes (`role="dialog"`, `aria-modal="true"`) to be accessible. Toggling CSS classes alone leaves keyboard users stranded.
**Action:** Always implement `keydown` listeners for Escape (close) and Tab (trap) when building custom modals. Consider refactoring to native `<dialog>` element for simpler browser-native accessibility in the future.
