## 2024-06-02 - Form Labels and Hint Accessibility
**Learning:** The flex-col layout separates labels from inputs visually, making explicit `for` attributes critical for accessibility. Form inputs like select elements also require `aria-describedby` to programmatically associate them with their helper text.
**Action:** Always add explicit `for` attributes to labels and `aria-describedby` to inputs that have hint text, ensuring reliable screen reader associations and clickable label areas.
