
## 2025-05-15 - Explicit Label Associations in Flex Layouts
**Learning:** When form inputs and their labels are visually separated (e.g., using Tailwind's `flex-col`), explicit `for` attributes on `<label>` elements are crucial for accessibility, as the spatial relationship is lost to screen readers. Similarly, hint text must be explicitly linked using `aria-describedby` on the input.
**Action:** Always ensure `<label>` has a `for` attribute matching the input's `id`, and hint text `id` is referenced in the input's `aria-describedby`, especially when the elements are not physically adjacent in the DOM or are visually separated by layout styles.
