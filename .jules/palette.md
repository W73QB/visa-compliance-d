## 2025-03-04 - Screen Reader Context in flex-col Layouts
**Learning:** Form inputs separated from their visual labels using `flex-col` and gap styling lose their implicit association for screen readers, meaning users hear the input name but not the descriptive context or help text.
**Action:** Always add explicit `<label for="[id]">` and link helper text with `aria-describedby="[id]"` to native `<select>` and `<input>` elements when using layout utility classes that visually disconnect them.
