## 2024-05-15 - Form Select Accessibility Improvements
**Learning:** Found that custom-styled native `<select>` elements in the main form lacked explicit `<label for="...">` associations and `aria-describedby` links to their helper hints, reducing screen reader utility and violating accessibility standards. Form inputs grouped physically but separated functionally require explicit semantic linkage.
**Action:** Always ensure that `<label>` elements have a corresponding `for` attribute and that hint text (`<p id="...">`) is linked via `aria-describedby` to its input element.
