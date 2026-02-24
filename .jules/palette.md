## 2026-02-24 - Material Symbols Accessibility
**Learning:** Google Material Symbols are implemented as ligatures (text content in spans). Screen readers announce the icon name (e.g., "gavel") unless explicitly hidden.
**Action:** Always add `aria-hidden="true"` to `material-symbols-outlined` spans that are decorative.
