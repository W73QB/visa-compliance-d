
## 2025-02-28 - [Accessible Labels and Descriptions for Flex-Col Dynamic Selects]
**Learning:** Due to the `flex-col` layout visually separating the label, dynamic `<select>` input, and helper text, implicit label wrapping is insufficient. Explicit `for` attributes on the `<label>` and `aria-describedby` attributes on the `<select>` referencing the helper text ID are critical to ensure screen readers properly announce the input purpose and context before the dynamic options are fully populated.
**Action:** When creating dynamic form inputs (especially selects) with associated helper text and separated visual layouts, always explicitly bind labels with `for` and helper hints with `aria-describedby`.
