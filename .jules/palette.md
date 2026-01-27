## 2026-01-26 - Modal Focus Management
**Learning:** Modals that don't trap or manage focus leave keyboard users lost (focus stays on the trigger button behind the backdrop). Adding `aria-modal="true"` and moving focus to the modal/close button is essential for context switching.
**Action:** Always save `document.activeElement` before opening a modal and restore it upon closing. Ensure the modal or its first interactive element receives focus immediately after opening.
