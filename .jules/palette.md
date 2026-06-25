## 2024-06-25 - Accessibility fixes for UI components
**Learning:** Form `<label>` associations and input hints require explicit attributes (`for` and `aria-describedby`), especially when visual flex layouts decouple them. Mobile menu toggles also need synchronized `aria-expanded` attributes in their JS logic.
**Action:** Add strict tests for proper ARIA/label relationships when introducing new semantic components.
