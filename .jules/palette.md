## 2024-06-03 - Added ARIA attributes to mobile menu and check button
**Learning:** Interactive elements that toggle visibility (like mobile menus) or change states (like submit buttons) can cause confusion for screen reader users if `aria-expanded` and `aria-disabled` attributes are missing or not kept in sync dynamically alongside visual class or property changes.
**Action:** Ensure dynamic components are audited for correct ARIA state management so screen reader context accurately reflects visual state.
