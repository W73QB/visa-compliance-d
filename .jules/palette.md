## 2026-03-17 - Added label 'for' and 'aria-describedby' to ui/index.html forms
**Learning:** Due to the flex-col layout in this app separating labels visually from inputs, clicking a label without a 'for' attribute fails to focus the select input, and screen readers fail to associate helper text due to missing 'aria-describedby' attributes on selects.
**Action:** When working on form inputs here, specifically `<select>` wrapped with icons/styling, ensure explicit `for="id"` and `aria-describedby="hintId"` links are present.
