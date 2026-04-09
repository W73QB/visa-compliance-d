## 2024-05-14 - Explicit Label Associations in Complex Layouts
**Learning:** Due to the `flex-col` layout in `ui/index.html` separating labels from their inputs visually, native `<label>` wrapping is insufficient or risky for accessibility. Form elements like `<select>` require explicit `for` attributes on the label and `aria-describedby` linking to helper text for proper screen reader communication.
**Action:** Always verify explicit `for` bindings for labels and add `aria-describedby` for inputs with helper text, especially in custom or complex CSS flex/grid layouts.
