
## 2024-05-04 - Accessibility Enhancements for Material Symbols and Form Inputs
**Learning:** Material Symbols loaded via `<span>` tags as ligatures are read aloud by screen readers as the underlying text (e.g., "verified user") and must have `aria-hidden="true"` applied to be skipped. Additionally, form inputs like `<select>` in this application's layout need `for` attributes on their separated label tags and `aria-describedby` linked to their helper hints to properly describe the input's context to screen reader users.
**Action:** When adding material symbols, ensure `aria-hidden="true"` is applied to the span. Always associate separate label texts to input tags via `for` and `id`, and link helper text with `aria-describedby` to input tags to ensure full form accessibility.
