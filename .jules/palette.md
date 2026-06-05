
## 2023-10-24 - Accessibility bindings for inputs and buttons
**Learning:** Found an accessibility issue pattern where inputs inside complex flex layouts were missing `for` labels, and dynamic menu buttons were missing `aria-expanded` attributes. Also, dynamically disabling a button (`btn.disabled = true`) doesn't always announce its inactive state properly on some screen readers without `aria-disabled="true"`.
**Action:** Added exact label `for` bindings to `id`s, `aria-describedby` to inputs, and bound `aria-expanded` tracking dynamically to the mobile menu open state class toggling.
