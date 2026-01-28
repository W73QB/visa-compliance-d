## 2026-01-28 - Manual Modal Focus Management
**Learning:** Vanilla JS modals require explicit focus management (trap, restore, escape) which is often overlooked compared to using libraries.
**Action:** Always implement `keydown` listeners for Tab/Escape and store/restore `document.activeElement` when building custom modals.
