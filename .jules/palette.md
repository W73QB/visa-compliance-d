## 2024-06-24 - Interactive Component Accessibility
**Learning:** Icon-only toggles and form elements without explicit label associations require proper ARIA attributes to be fully accessible. Dynamic state requires syncing JavaScript (`aria-expanded`) and explicit target matching (`aria-controls`, `aria-describedby`, and `for`).
**Action:** Always add ARIA attributes and explicitly link inputs, toggles, and elements that they control or are described by.
