## 2024-03-20 - Ensure Material Icons are Accessible
**Learning:** Google Material Symbols are implemented as ligatures within `<span>` tags. Without `aria-hidden="true"`, screen readers will announce the icon name (e.g. "verified_user", "menu", "warning") as text, which is confusing and poor UX, especially for icon-only buttons or decorative icons.
**Action:** Always add `aria-hidden="true"` to elements with `class="material-symbols-outlined"` in the `ui/index.html` file.
