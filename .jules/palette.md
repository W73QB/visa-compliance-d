## 2024-05-18 - Missing ARIA attributes for Material Symbols
**Learning:** Google Material Symbols are implemented as ligatures within `<span>` elements (e.g., `<span class="material-symbols-outlined">rule</span>`). Screen readers will announce the literal text "rule" rather than treating it as a decorative icon unless `aria-hidden="true"` is applied.
**Action:** Always add `aria-hidden="true"` to Google Material Symbol `<span>` tags.

## 2024-05-18 - Missing labels in Form Inputs
**Learning:** The form inputs (like `visaSelect` and `productSelect`) visually group the label and the select element, but the labels are missing a `for` attribute (e.g., `<label for="visaSelect">`) tying them to the respective inputs, causing accessibility issues.
**Action:** Add `for` attributes to labels to properly link them to `<select>` or `<input>` elements.
