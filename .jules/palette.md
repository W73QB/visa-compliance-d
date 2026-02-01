## 2025-05-15 - Manual Modal Accessibility
**Learning:** The application uses a custom vanilla JS modal without `dialog` element or accessibility libraries. Manual implementation of `role="dialog"`, `aria-modal`, and focus trap is required for every modal.
**Action:** When creating or modifying modals in `ui/index.html`, explicitly implement `handleModalKeydown` for Tab (focus trap) and Escape (close), and manage `document.activeElement` restore.
