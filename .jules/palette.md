## 2026-05-22 - Accessibility Gaps in Custom Modals
**Learning:** Custom modal implementations often miss critical accessibility features like `aria-modal="true"`, `role="dialog"`, focus management (trap/restore), and Escape key handling, making them inaccessible to keyboard and screen reader users.
**Action:** Always verify custom interactive components (like modals) against WAI-ARIA authoring practices and ensure focus management is implemented explicitly.

## 2026-05-22 - Form Label Association
**Learning:** Visual labels near form inputs are insufficient for accessibility; explicit `for` attributes linking `label` to `input` ID are mandatory for screen readers.
**Action:** Verify all form inputs have associated labels using automated checks or code review.
