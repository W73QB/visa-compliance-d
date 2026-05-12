## 2024-05-01 - Material Symbols Require ARIA Hidden
**Learning:** Google Material Symbols are implemented as ligatures in `<span>` tags (e.g., `<span class="material-symbols-outlined">menu</span>`). Screen readers will announce the literal text "menu" unless explicitly hidden.
**Action:** Always add `aria-hidden="true"` to Material Symbols spans to prevent confusing screen reader announcements.

## 2024-05-01 - Missing ARIA Labels on Icon Buttons
**Learning:** Buttons containing only Material Symbols for visual representation (e.g., `#mobileMenuBtn`) lack accessible names for screen reader users.
**Action:** Add explicit `aria-label` attributes to icon-only buttons to provide context.
