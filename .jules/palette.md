## 2024-05-24 - Add ARIA accessibility to form and menu
**Learning:** Form labels using visual proximity instead of explicit `for` attributes fail screen reader tests, and mobile menu toggles need `aria-controls` and dynamic `aria-expanded` attributes to convey their state.
**Action:** Always add explicit `for="[id]"` attributes to labels and `aria-describedby` for hint text, and ensure interactive toggles programmatically reflect their visual state changes using `setAttribute('aria-expanded', String(!isOpen))`.
