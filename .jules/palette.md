## 2023-10-24 - Add ARIA attributes to mobile menu button
**Learning:** Icon-only toggle buttons in responsive layouts (like the mobile menu) often rely purely on visual class changes (`md:hidden`, `hidden`) without conveying state changes to screen readers, leaving them inaccessible.
**Action:** When implementing dynamic interactions, ensure visual state changes are mapped to corresponding ARIA attributes (e.g., `aria-expanded`, `aria-controls`) programmatically in the JavaScript logic.
