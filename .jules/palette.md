## 2025-02-19 - Form Accessibility and Material Symbols

**Learning:** When form labels are visually separated from inputs (e.g., using Tailwind `flex-col` layout), explicit `for` attributes and `aria-describedby` associations are crucial for screen readers to provide context. Furthermore, Google Material Symbols implemented as ligatures inside `<span>` tags must include `aria-hidden="true"` to prevent screen readers from reading the icon names as literal text (e.g., "verified user").
**Action:** Always ensure inputs have associated labels via explicit `for` attributes, and use `aria-describedby` for hint text. Consistently add `aria-hidden="true"` to decorative icon fonts.
