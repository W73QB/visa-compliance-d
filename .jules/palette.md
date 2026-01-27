## 2026-01-27 - Manual Modal Accessibility
**Learning:** The existing `ui/index.html` used a plain `div` for modals without any accessibility attributes or focus management, making it invisible to screen readers and trapping keyboard users.
**Action:** When working with vanilla JS modals, always implement `role="dialog"`, focus trapping (Tab loop), `Escape` key listener, and focus restoration to trigger element.
