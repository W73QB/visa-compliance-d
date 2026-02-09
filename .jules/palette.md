## 2026-02-09 - Vanilla JS Modals
**Learning:** This app uses vanilla JS for modals in a single file (`ui/index.html`). Manual focus management (trap, restore) and ARIA attributes are required for accessibility as no framework handles this.
**Action:** When touching modals, always verify `keydown` listeners for Escape and focus restoration logic.
