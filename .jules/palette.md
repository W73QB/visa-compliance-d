
## 2026-03-09 - [Material Symbols and Form Hint Accessibility]
**Learning:** Material Symbols implemented via ligatures (e.g. `<span class="material-symbols-outlined">rule</span>`) are announced by screen readers as the text content ("rule") unless explicitly hidden. Additionally, the standard `flex-col` layout separates inputs from their instructional hints (`<p id="hint">`), meaning screen readers miss the hints without `aria-describedby` connecting them.
**Action:** Always add `aria-hidden="true"` to structural/decorative font icons, and always map instructional text explicitly using `aria-describedby` on the corresponding input element.
