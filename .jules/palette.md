## 2024-06-16 - Accessibility improvements for mobile menu and form selects
**Learning:** Input labels in flex-col layouts require explicit `for` attributes for accessibility to properly associate with inputs. Icon-only interactive buttons like mobile menus need `aria-controls` and dynamic `aria-expanded` attributes to convey their state to screen readers.
**Action:** Always ensure custom styled `<select>` or `<input>` fields have a corresponding `<label for="...">` and helpful text mapped with `aria-describedby`. Ensure dynamic toggles update `aria-expanded`.
