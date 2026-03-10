
## $(date +%Y-%m-%d) - Evidence Modal Accessibility
**Learning:** Adding explicit `role="dialog"`, `aria-modal="true"`, and keyboard support (`Escape` to close, restore focus on close) makes custom modals compliant and accessible, whereas missing these causes screen readers to ignore the modal trap and trap keyboard users.
**Action:** Always include complete ARIA modal attributes and lifecycle focus management when building custom modals without native `<dialog>` tags.
