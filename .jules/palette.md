## 2024-06-11 - Dynamic ARIA attributes for mobile menus
**Learning:** Icon-only toggle buttons like `#mobileMenuBtn` not only need an `aria-label`, but they MUST explicitly manage their `aria-expanded` and `aria-controls` state dynamically in JS, so screen readers announce when the targeted component (#mobileMenu) opens or closes.
**Action:** Always add `aria-expanded="false"` and `aria-controls="targetID"` to toggle buttons, and update the `aria-expanded` attribute within the click handler to `String(!isOpen)` or the equivalent boolean expression reflecting the NEW state.
