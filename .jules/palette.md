## 2024-05-23 - Custom Modal Accessibility
**Learning:** Custom modal implementations often lack invisible accessibility features like focus trapping and keyboard navigation (Escape key), making them unusable for keyboard-only users.
**Action:** Always wrap custom modals with `role="dialog"`, `aria-modal="true"`, and implement explicit focus management (trap + restore) and Escape key listeners.
