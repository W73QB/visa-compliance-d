## 2026-04-20 - Material Symbols Accessibility
**Learning:** Material Symbols are implemented as ligatures within `<span>` tags. Screen readers will literally read the text content like "menu" or "verified_user" out loud to the user unless they are explicitly hidden.
**Action:** Add `aria-hidden="true"` to all material symbol `<span>` tags to prevent confusing screen reader announcements.
