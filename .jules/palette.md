## 2026-01-24 - Accessibility Patterns for Static Modals
**Learning:** Static modals without a framework require manual focus management (save/restore) and explicit ARIA attributes (`role="dialog"`, `aria-modal="true"`) to be accessible. Simply hiding/showing via CSS is insufficient for screen readers.
**Action:** Always implement focus restore and ARIA attributes when building custom modals in vanilla JS.
