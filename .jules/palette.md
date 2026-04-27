## 2024-05-19 - Form Accessibility Enhancements
**Learning:** Input labels in `ui/index.html` lacked explicit `for` attributes (required due to flex-col layout) and select elements lacked `aria-describedby` links to their hint text. Furthermore, the `#checkBtn` disabled state lacked `aria-disabled="true"`.
**Action:** Ensure all labels have `for` attributes referencing their input IDs, connect form inputs to hints using `aria-describedby`, and programmatically manage `aria-disabled` on dynamically enabled/disabled buttons.
