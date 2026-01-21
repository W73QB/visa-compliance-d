## 2026-01-21 - Accessible Modals
**Learning:** Modals require manual focus management (save/restore) and `aria-modal="true"` to be truly accessible to keyboard and screen reader users. Standard HTML/CSS hiding isn't enough.
**Action:** Always include focus trapping (or at least focus moving) and Escape key listeners when implementing custom modals.
