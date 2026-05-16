## 2024-05-16 - Ensure dynamic interactions map visual states to ARIA attributes
**Learning:** When implementing dynamic interactions like toggleable menus, visual class changes (e.g., hidden) must be mapped to their corresponding ARIA attributes (e.g., `aria-expanded`) programmatically in the JavaScript logic to ensure full accessibility for screen readers.
**Action:** Always verify that buttons controlling collapsible content have `aria-controls` and a dynamically updating `aria-expanded` attribute that mirrors the visual state of the controlled element.
