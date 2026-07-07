## 2026-07-07 - Form Accessibility Labels
**Learning:** Form inputs styled flexibly without wrapping labels require explicit `for` attributes and `aria-describedby` to correctly associate them with hint text for screen readers. Dynamic ARIA attributes like `aria-expanded` need programmatic updates reflecting their newly toggled states in JavaScript logic.
**Action:** Ensure all detached inputs get explicit `for` labels and associate context with `aria-describedby`. Update ARIA state logically via JS where visual toggle occurs.
