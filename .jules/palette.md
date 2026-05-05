## 2025-05-05 - Flex-col Layouts and Input Labels
**Learning:** In Tailwind designs, using `flex-col` to vertically stack labels and inputs visually disconnects them. This completely breaks implicit click-to-focus behavior for `<label>` elements unless an explicit `for` attribute maps directly to the input's `id`.
**Action:** Always ensure an explicit `for` attribute is added to `<label>` elements when they are separated from their inputs via block or flex wrappers.
