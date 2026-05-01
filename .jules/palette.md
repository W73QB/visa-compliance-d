## 2024-05-01 - Flex-col layout separating labels from inputs requires explicit associations
**Learning:** The `flex-col` layout in `ui/index.html` separates labels from inputs visually, which creates an accessibility risk requiring explicit `for` attributes on `<label>` elements to associate them with input `id`s, as well as `aria-describedby` on inputs to link to hint text.
**Action:** When implementing inputs with visually separated labels or helper text, always use `for` and `aria-describedby` attributes to ensure programmatic association.
