## 2026-05-25 - Prevent screen readers from reading Material Symbol ligatures
**Learning:** Google Material Symbols are implemented as text ligatures in <span> tags, causing screen readers to announce the raw icon name (e.g. 'menu' or 'check_circle').
**Action:** Always add aria-hidden="true" to Material Symbol icons to hide them from screen readers, pairing them with an aria-label on the parent button if they are interactive.
