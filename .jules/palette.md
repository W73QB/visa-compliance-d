## 2026-04-15 - Explicit form labels required for flex-col layouts
**Learning:** In flex-col layouts where inputs and their labels are visually grouped but structurally separated in the DOM, implicit labeling (wrapping input inside label) is not always used. Screen readers will fail to associate them.
**Action:** Always use explicit `for` attributes on labels pointing to the `id` of the input, and ensure helper texts are associated via `aria-describedby` on the input element.
