## 2026-04-07 - Google Material Symbols Ligature Accessibility
**Learning:** Google Material Symbols implemented as ligatures within `<span>` tags (e.g. `<span class="material-symbols-outlined">menu</span>`) will be read aloud by screen readers as the text content (e.g. "menu" or "verified user"), which is confusing when they are meant to be purely decorative or are already accompanied by descriptive text.
**Action:** Always add `aria-hidden="true"` to ligature-based icon elements to prevent screen readers from announcing the icon name as text.
