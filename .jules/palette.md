## 2026-01-16 - Form Field Association

**Learning:** When inputs and labels are separated by multiple DOM layers and flex/grid wrappers, screen reader associations fail unless explicit `for`/`id` linking is created for labels, and `aria-describedby` links hints to their corresponding form elements.

**Action:** Always ensure that `for` attributes on `<label>` point to their corresponding form controls (`id`), and `aria-describedby` attaches hint text (`<p>`) properly so users with screen readers don't miss context.
