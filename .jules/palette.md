## 2026-04-13 - Add Accessible Associations to Form Elements
**Learning:** The flex-col layout in this app causes labels to be visually disconnected from select menus, requiring explicit `for` attributes and `aria-describedby` hints for screen readers to properly context-switch into the complex interactive controls.
**Action:** When adding or updating custom `<select>` menus inside `.flex-col` containers, always pair `<label for="[id]">` and set `aria-describedby="[hint_id]"` on the interactive element.
