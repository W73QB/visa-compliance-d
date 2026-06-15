## 2024-05-23 - Form Accessibility in Flex-col Layouts
**Learning:** Input labels in ui/index.html without explicit for attributes fail to trigger corresponding input elements, which is especially problematic in flex-col layouts where labels and inputs are visually separated. Screen readers also miss hint texts if aria-describedby isn't used.
**Action:** Always include explicit for attributes on <label> elements matching input IDs, and use aria-describedby on inputs referencing their helper text elements.
