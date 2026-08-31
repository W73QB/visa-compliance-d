## 2026-07-04 - Dynamic ARIA Attributes for Toggles
**Learning:** Visual toggle states (e.g., mobile menus) must have their ARIA attributes (like `aria-expanded`) dynamically updated via JavaScript to ensure screen readers stay synced with the visual state.
**Action:** When adding class-based toggles, always update the corresponding ARIA attributes in the same event handler.
