## 2026-01-20 - Dynamic ARIA toggles on mobile menus
**Learning:** The mobile menu toggle button requires dynamic updates to `aria-expanded` and explicit `aria-controls` mapping for full screen reader accessibility, particularly since it was originally styled just with visual utility classes.
**Action:** Ensure all interactive layout toggles include dynamic ARIA attribute synchronization in their JavaScript handlers.
