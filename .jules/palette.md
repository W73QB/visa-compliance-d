## 2026-02-27 - Modal Accessibility Pattern
**Learning:** Native `role="dialog"` and `aria-modal="true"` are critical for screen readers, but incomplete without focus management. The combination of trapping focus (implicit with aria-modal in some readers, but explicit management is better), restoring focus on close, and handling the Escape key creates a robust, accessible modal pattern.
**Action:** When implementing custom modals, always pair ARIA attributes with `keydown` (Escape) listeners and `lastFocusedElement` tracking to restore context for keyboard users.
