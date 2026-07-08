## 2026-07-08 - Form Input Accessibility
**Learning:** The flex-col layout in the main UI form visually separates labels from their inputs, making explicit associations critical for screen readers, and inputs are missing semantic links to their helper text.
**Action:** Always add `for` attributes to labels and `aria-describedby` to inputs referencing their helper text, especially when using complex CSS layouts.
