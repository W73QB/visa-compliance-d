## 2024-05-22 - Modal Accessibility Pattern
**Learning:** This application uses custom HTML/JS modals instead of native `<dialog>` or a library. Critical accessibility features (focus management, ARIA roles, focus trapping) are missing by default.
**Action:** When working on modals in this repo, always manually implement:
1. `role="dialog"` and `aria-modal="true"` on the container.
2. `aria-labelledby` pointing to the modal title.
3. Save `document.activeElement` on open.
4. Move focus to the modal (or its first interactive element) on open.
5. Restore focus to the saved element on close.
6. Handle `Escape` key to close.
