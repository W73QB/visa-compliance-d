## 2026-05-22 - Improved Semantic HTML Association and ARIA Toggles
**Learning:** Adding explicit `for` attributes to `<label>` tags linked to native `<select>` elements greatly improves focus flow and screen-reader association. Additionally, directly toggling attributes like `aria-expanded` and `aria-disabled` synchronously with their visual states creates a much better semantic experience.
**Action:** When creating form inputs or dynamically updating visual indicators like disabled buttons and mobile menus, immediately ensure `aria-` properties are synced as well.
