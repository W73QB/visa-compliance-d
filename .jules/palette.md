## 2025-03-21 - [Form Labels & ARIA Context]
**Learning:** Found that `<label>`s for standard inputs inside flex columns lack explicit `for` attributes and missing `aria-describedby` relations, failing to link label interaction and helpful context texts correctly for assistive technologies.
**Action:** Always verify explicit `for` bindings are present and connect contextual hints using `aria-describedby` instead of relying merely on visual proximity, specifically in this app's Tailwind-styled input wrappers.
