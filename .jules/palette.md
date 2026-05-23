
## 2026-01-20 - Adding explicit ARIA attributes and missing labels
**Learning:** Dynamic UI components (e.g. mobile menus, disabled buttons) that change classes do not automatically convey their new state to screen readers. Furthermore, decorative icons implemented with span tags containing text ligatures (e.g., Google Material Symbols) get read as arbitrary words if they are not explicitly hidden via `aria-hidden="true"`.
**Action:** Always add explicit `aria-expanded`/`aria-controls` for dropdowns, map `disabled` to `aria-disabled="true"`, explicitly hide font-icon ligatures, and bind labels to inputs using explicit `for` and `aria-describedby` tags.
