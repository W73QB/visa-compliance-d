## 2024-06-25 - ARIA attributes on dynamic elements
**Learning:** For dynamic interactions like `disabled` state toggling on buttons or expandable menus, using ARIA attributes like `aria-disabled` and `aria-expanded` is essential to properly convey the state change to screen reader users, especially when the visual classes change simultaneously.
**Action:** Always map visual state changes (`hidden`, `disabled`, color changes) to equivalent ARIA states (`aria-hidden`, `aria-expanded`, `aria-disabled`) programmatically.
