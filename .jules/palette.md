## 2024-06-07 - Add accessibility attributes to mobile menu toggle
**Learning:** Icon-only toggle buttons in the UI like `#mobileMenuBtn` need explicit `aria-expanded` and `aria-controls` attributes for full accessibility.
**Action:** Added `aria-expanded="false"` and `aria-controls="mobileMenu"` to the `#mobileMenuBtn` element, and programmatically update `aria-expanded` state on click.
