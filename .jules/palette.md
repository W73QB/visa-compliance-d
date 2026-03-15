## 2026-03-15 - [Form Label Associations in Flex Layouts]
**Learning:** Using flex-col layouts often creates visual separation between labels and inputs, masking missing programmatic associations. Inputs (like select) require explicit `for` and `id` linking for screen readers to properly associate the visual label with the input element.
**Action:** Always verify `for` attributes on form labels exist and map to a valid input `id`, regardless of visual proximity. Also, ensure helper text is explicitly linked to form controls via `aria-describedby` since visual grouping alone is not accessible.
