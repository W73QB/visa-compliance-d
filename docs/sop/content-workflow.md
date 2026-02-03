# SOP: Content Upgrade Workflow

## DeepResearch -> Write (2-step)

### Step A: DeepResearch (research-only)

Output bắt buộc:

- Danh sách primary sources (ưu tiên cơ quan ngoại giao/chinh phu/PDF)
- Bang Normalized Requirements:
  - Requirement (chuẩn hoa 1 cau)
  - URL
  - Locator
  - Verified date
- Danh sach claim chua du nguon -> UNKNOWN
- Trap candidates (neu suy luan thi gan nhan INFERENCE)

### Step B: Write (chi dung research da chot)

Output bắt buộc:

- Markdown bai theo template VisaFact
- FAQ (chi cau co nguon)
- JSON-LD FAQ (chi khi FAQ du bang chung)
- Evidence log cuoi bai

Quy tac: khong viet bai neu chua co Normalized Requirements Table.

---

## Template 11 blocks (bat buoc)

1. Short answer (2-3 cau)
2. Key findings at a glance (bang)
3. What the authority requires (3-8 bullet, moi bullet co source + locator + verified date)
4. Verified requirements (checklist PASS/FAIL/UNKNOWN)
5. How we evaluate (rule engine + UNKNOWN > Wrong)
6. Proof package checklist (chi muc co nguon)
7. Common rejection traps (neu inference phai gan nhan)
8. FAQ (4-6 cau)
9. Check in the engine (link placeholder)
10. Disclaimer + Affiliate disclosure
11. Evidence log

---

## Quality gate (pass/fail)

### Claim audit

- Moi cau must/required/not accepted phai co nguon + locator
- Khong khang dinh vuot qua nguon
- Neu co route variability phai neu ro
- Thoi han toi thieu chi noi khi co nguon, neu khong -> UNKNOWN

### Proof-read theo chuan compliance

- Bai quy ve: cai gi co the chung minh bang giay to
- Cho certificate/letter phai co nguon
- Neu nguon noi "we won't read fine print" thi nhan manh proof must be explicit

### SEO + UX gate

- Title/meta dung intent
- FAQ 4-6 cau dung query
- Internal links 5-8 link/bai
- Co Related block
- Co Last updated
