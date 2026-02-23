## 2026-02-23 - Form Accessibility Fundamentals
**Learning:** Decorative icons in form inputs can create noise for screen readers, and unassociated labels break the expected interaction pattern (click-to-focus).
**Action:** Always add `aria-hidden="true"` to decorative icons inside inputs and ensure every `label` has a `for` attribute matching its input ID.
