## 2024-05-23 - Accessible Modal Focus Management
**Learning:** Modals must explicitly manage focus (trap on open, restore on close) and provide `aria-modal="true"`. Simply toggling visibility is not accessible for keyboard and screen reader users.
**Action:** Always implement `openModal` with focus saving and `closeModal` with focus restoration. Use `aria-labelledby` to point to the modal title.
