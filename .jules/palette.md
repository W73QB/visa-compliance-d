## 2025-05-15 - [Form Input Accessibility]
**Learning:** The flex-col layout separates visual labels from their input elements (`<select>`). Explicit `for` attributes and `aria-describedby` are critical to ensure screen readers associate hints and labels correctly.
**Action:** Always verify custom form components that use flex layouts to group elements have hardcoded `for` attributes on labels targeting input IDs. Also update Javascript toggles for `disabled` state to sync with `aria-disabled` for accessibility.
