# Palette's Journal

## 2026-01-18 - Accessible Modal Focus Management
**Learning:** Modals in this static setup require manual focus management (trap and restore) to be accessible, as there is no framework handling it.
**Action:** Always implement `handleModalKeydown` (trap) and save/restore `document.activeElement` for any new overlay components.
