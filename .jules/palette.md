## 2026-06-06 - Form Input Accessibility
**Learning:** Flex-col layouts visually separate labels from inputs, making explicit `for` and `aria-describedby` attributes essential for screen reader context. Icon-only mobile buttons must also dynamically update `aria-expanded` and reference `aria-controls`.
**Action:** Ensure all form labels use the `for` attribute referencing an input ID, and inputs use `aria-describedby` referencing helper text. Icon buttons toggling visibility need explicit ARIA state handling.
