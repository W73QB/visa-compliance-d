## 2025-02-18 - Accessible Modal Pattern
**Learning:** Implemented a robust focus trap and ARIA attributes for the Evidence modal. This pattern (saving active element, trapping Tab/Shift+Tab, restoring focus on close) is essential for keyboard accessibility in vanilla JS overlays.
**Action:** Reuse `handleModalKeydown` logic for any future overlay components (e.g., custom dropdowns, side panels).
