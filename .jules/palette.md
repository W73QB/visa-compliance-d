## 2024-05-18 - Missing ARIA attributes for Selects and Material Icons
**Learning:** Google Material Symbols are implemented as ligatures in `span` tags and will be read out as raw text by screen readers unless hidden with `aria-hidden="true"`. Also, form layout components relying on sibling hints benefit from `aria-describedby` for robust accessibility.
**Action:** Always ensure all material symbol spans receive `aria-hidden="true"`. Add explicit label mappings (`for="[id]"`) for stacked select layouts to ensure screen readers focus inputs properly.
