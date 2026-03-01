## 2026-03-01 - [Material Symbols Accessibility]
**Learning:** Google Material Symbols in this project are implemented using ligatures within `<span>` tags. Without explicitly applying `aria-hidden="true"`, screen readers will announce the raw text (e.g., "verified_user", "menu"), creating a confusing and poor experience for non-sighted users. This issue applies to all `class="material-symbols-outlined"` elements, especially those used purely for decoration.
**Action:** Always ensure that decorative `<span class="material-symbols-outlined">` tags include `aria-hidden="true"`.
