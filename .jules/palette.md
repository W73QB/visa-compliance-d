## 2026-02-05 - Missing Modal Accessibility
**Learning:** The custom vanilla JS modal implementation lacked basic accessibility features (ARIA roles, focus management, Escape key support), creating a barrier for keyboard and screen reader users.
**Action:** When working with custom interactive components in this codebase, explicitly check for and implement ARIA attributes and focus management, as the base implementation is minimal.
