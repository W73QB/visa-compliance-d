## 2024-04-29 - Fixed Label-to-Input Association for Selects
**Learning:** The `flex-col` layout visually separates labels from inputs, but screen readers require explicit programmatic association. Relying on visual proximity is insufficient for accessibility, particularly for form components like `<select>`.
**Action:** Always ensure that inputs, particularly those in `flex-col` or visually distinct layouts, have explicit `for` attributes on their corresponding `<label>` elements and utilize `aria-describedby` to link any associated hint or helper text.
