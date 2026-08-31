## 2024-06-14 - Explicit Label Associations in Flex Columns
**Learning:** Input labels require explicit `for` attributes to trigger the corresponding input element for accessibility, particularly when they are visually separated by `flex-col` layouts. Also, form inputs need `aria-describedby` referencing their hint text elements.
**Action:** Always ensure `<label>` elements use the `for` attribute pointing to the ID of the input, and inputs use `aria-describedby` pointing to the ID of associated helper text.
