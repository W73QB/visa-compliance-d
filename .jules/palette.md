
## 2024-05-18 - Explicit Label Associations in Flex Layouts
**Learning:** In responsive designs where labels and inputs are separated visually (e.g., using `flex-col` with gaps), screen reader users and those navigating by touch lose the contextual association. Wrapping inputs in labels isn't always possible when using complex wrapper divs for icons.
**Action:** Always use explicit `for` and `id` pairing on forms, and ensure hint text is explicitly associated via `aria-describedby`, particularly when custom styling separates the semantic flow.
