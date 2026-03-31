## 2025-02-19 - Explicit Form Labels
**Learning:** Found critical form inputs (`visaSelect`, `productSelect`) with visual labels that lacked programmatic association (`for` attribute). This breaks screen reader support despite looking correct visually.
**Action:** When auditing forms, programmatically verify `label[for]` matches `input[id]`, do not rely on visual proximity or DOM nesting alone.
