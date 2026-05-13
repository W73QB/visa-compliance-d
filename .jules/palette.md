## 2024-05-13 - Missing ARIA attributes on dynamic mobile menus
**Learning:** Icon-only buttons used for mobile menus must include `aria-expanded` and `aria-controls` explicitly linked to the menu content, and ensure JS updates `aria-expanded` based on visibility.
**Action:** Always map toggleable visual states (like hidden/visible menus) to ARIA attributes programmatically and add `aria-expanded`/`aria-controls` to the toggle button.
