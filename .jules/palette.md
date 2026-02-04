## 2026-02-04 - Accessible Modal Implementation
**Learning:** Vanilla JS modals require manual focus management (trap focus, restore focus) and ARIA attributes (`role="dialog"`, `aria-modal="true"`) to be accessible. Simply showing/hiding a div is insufficient for screen readers and keyboard users.
**Action:** Always implement a `handleKeydown` function for `Tab` (trap) and `Escape` (close) when building custom modals, and ensure focus is restored to the triggering element on close.
