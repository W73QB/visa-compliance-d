
## 2024-03-24 - Accessibility Enhancements
**Learning:** Input labels in flex layouts require explicit `for` attributes for proper screen reader association. Form inputs need `aria-describedby` referencing hint texts. Mobile menu toggle buttons require `aria-expanded` and `aria-controls` to programmatically expose their state.
**Action:** Ensure custom dropdowns/selects and toggle buttons implement comprehensive ARIA properties when native association falls short.
