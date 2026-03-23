## 2024-03-24 - Google Material Icons Need aria-hidden
**Learning:** Google Material Icons are implemented via ligature fonts (e.g. `<span class="material-symbols-outlined">menu</span>`). This causes screen readers to announce the ligature text (e.g. "menu") confusingly alongside actual visually hidden or descriptive text, reducing accessibility.
**Action:** Always add `aria-hidden="true"` to ALL Google Material symbol spans to hide them from assistive technologies, ensuring the visually hidden or aria-labels provide the sole context for screen readers.
