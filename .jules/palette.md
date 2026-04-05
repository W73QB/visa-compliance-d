
## 2026-04-05 - Dynamic Select Input Helper Text Accessibility
**Learning:** In a UI where select elements have dynamic helper texts that update based on user choices, `aria-describedby` must be used to link the `<select>` element to its helper `<p>` text to provide context to screen reader users when navigating form elements. Additionally, for inputs with separate label elements, explicit `for` attributes are critical for establishing programmatic associations, especially when styled in flex columns where labels and inputs might not be implicitly nested.
**Action:** Always verify `aria-describedby` when a helper text block is structurally near an input but not semantically connected, and ensure `<label>` elements use explicit `for` mappings matching the input `id`.
