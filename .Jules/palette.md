# Palette's Journal

## 2024-05-22 - Accessibility Wins in Static Sites
**Learning:** In a vanilla JS static site without a framework, managing focus for modals requires manual intervention (`document.activeElement`). It's easy to forget but critical for keyboard users.
**Action:** Always check if a modal implementation includes focus trapping (or at least focus restoration) and `aria-modal="true"`.

## 2024-05-22 - Loading States for Async Data
**Learning:** For inputs populated by async fetch, showing an empty dropdown or static default text can be confusing. Explicit "Loading..." text provides immediate feedback.
**Action:** Initialize dynamic inputs with a "Loading..." placeholder that is cleared when data arrives.
