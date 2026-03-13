## 2026-03-13 - [Google Material Symbols a11y]
**Learning:** Google Material Symbols implemented as ligatures in `<span>` tags (e.g. `<span class="material-symbols-outlined">verified_user</span>`) are read literally by screen readers as the underlying text ("verified user"). This causes confusion, especially when used purely decoratively or next to explicit text.
**Action:** Always add `aria-hidden="true"` to such decorative font icons so that screen readers skip reading the ligature string.
