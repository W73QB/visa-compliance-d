## 2026-01-22 - Modal Accessibility & Encoding Quirks
**Learning:** `ui/index.html` relies on CRLF line endings. Changing them can cause diff noise. Also, regex range literals like `/[ - ]/` (space to space) can be misinterpreted or cause syntax errors; hex codes `/\x00-\x1F/` are safer.
**Action:** When editing `ui/index.html`, preserve CRLF line endings and use hex codes for control character ranges in regex.
