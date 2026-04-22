## 2024-04-22 - Missing 'for' attributes on labels
**Learning:** Found `<label>` elements without `for` attributes in `ui/index.html` referencing `<select>` elements (`#visaSelect` and `#productSelect`). The `flex-col` layout separates labels from inputs visually, so programmatic linkage is important.
**Action:** Adding explicit `for` attributes to connect labels to their corresponding inputs for improved accessibility.
