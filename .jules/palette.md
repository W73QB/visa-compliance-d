## 2026-07-02 - Mobile Menu ARIA Attributes
**Learning:** Icon-only toggle buttons like the mobile menu must dynamically update their `aria-expanded` state along with `aria-controls` to remain accessible to screen readers when the menu visibility changes.
**Action:** When adding toggleable UI elements, ensure visual state changes are mapped to corresponding ARIA attributes programmatically.
