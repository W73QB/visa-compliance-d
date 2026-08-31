## 2025-06-21 - Initialization\n**Learning:** Palette agent initialized.\n**Action:** Starting UX checks.

## 2025-06-21 - Form Labels and Menu Accessibility
**Learning:** Input labels in ui/index.html require explicit for attributes due to flex-col layout separating labels from inputs visually. Form inputs require aria-describedby for their hint texts. Icon-only buttons (like mobile menu) need aria-expanded and aria-controls for screen readers.
**Action:** Add explicit for/id associations to form elements and dynamic ARIA state to interactive menu buttons.
