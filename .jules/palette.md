## 2024-05-22 - Modal Accessibility Gaps
**Learning:** Custom modals in `ui/index.html` were implemented without focus management (no trap, no escape key support, no focus restoration).
**Action:** When modifying or adding modals, ensure `role="dialog"`, `aria-modal="true"`, and implement focus trapping and keyboard listeners (Escape).
