## 2025-02-19 - Accessible Micro-Interactions & Forms
**Learning:** The flex-col layout separates labels from inputs visually, making explicit `for` attributes mandatory for screen readers. Icon-only buttons lacking dynamic `aria-expanded` attributes leave screen reader users unaware of menu toggles.
**Action:** Always map visual class toggles (`hidden`) to corresponding ARIA attributes (`aria-expanded`) programmatically. Ensure form inputs feature `aria-describedby` when hint text is available.
