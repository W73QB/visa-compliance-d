# Palette's Journal

## 2026-02-01 - Modal Accessibility in Vanilla JS
**Learning:** Custom modals implemented in vanilla JS often miss critical accessibility features like focus management (trap/restore) and Escape key handling, making them unusable for keyboard and screen reader users. Simply toggling `hidden` classes is insufficient.
**Action:** Always implement `role="dialog"`, `aria-modal="true"`, focus trap (or move focus to first interactive element), focus restoration on close, and Escape key listener for any custom modal.
