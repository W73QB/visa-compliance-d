# Kế hoạch Tăng trưởng 12 Tuần (Bản Khả thi) — Evidence-First Growth Playbook

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Tăng trưởng organic traffic và affiliate conversion trong 12 tuần, dựa trên dữ liệu hiện có (6 visa routes, 7 products, 42 mappings) mà không vi phạm nguyên tắc evidence-first.

**Architecture:** Hub/spoke content model — mỗi hub post dài (~450-650 từ) liên kết đến spoke pages (visa route pages, trap pages, guides) ngắn nhưng chắc evidence. Mọi nội dung đi qua lint + SEO audit pipeline hiện có. Mở rộng data trước khi mở rộng content.

**Tech Stack:** Hugo + PaperMod, Python tooling (validate.py, lint_content.py, seo_audit.py, build_mappings.py), GTM event tracking, JSON-LD schema (WebSite, Organization, BreadcrumbList, Article, FAQPage).

---

## Lưu ý về command (cross-platform)

- Trên macOS, thường **không có** `py`. Dùng `python3` thay thế.
- Trên Windows/CI, `py` có sẵn. Nếu không chắc, dùng launcher trong PowerShell (`tools/tests/_python.ps1`).

## Nguyên tắc First Principles

### Chân lý gốc (Musk-style)

1. **No source = UNKNOWN.** Mọi claim phải có evidence từ primary source. Không suy đoán.
2. **Data trước Content.** Không viết bài nếu chưa có visa_facts + product_facts + sources đầy đủ.
3. **Evidence density > Word count.** Đo bằng "evidence items per section", không bằng số từ.
4. **Pipeline là gate.** Mọi content phải pass: `validate.py` → `lint_content.py` → `seo_audit.py`. Nếu fail = không ship.
5. **Tăng trưởng compound.** Ưu tiên cải thiện content hiện có (đã có index) trước khi tạo mới.

### Ràng buộc kỹ thuật bắt buộc

| Ràng buộc | Chi tiết |
|-----------|----------|
| `content/visas/**/index.md` | Generated bởi tooling, KHÔNG edit tay. Chỉnh qua generator. |
| Lint required blocks | Mỗi bài phải có: "what the authority requires", "how we evaluate", "check in the engine", "disclaimer", "affiliate disclosure" |
| Banned words | `best`, `recommend`, `recommended`, `guarantee`, `guaranteed`, `100%`, `approved`, `surely` — cấm trong content + offers |
| Deep links | Phải có `snapshot=` parameter |
| Schema JSON-LD | Đã có: WebSite, Organization, BreadcrumbList, Article, FAQPage. Thêm FAQ frontmatter khi có Q&A content. |
| SEO thresholds | Word count per file trong `seo_thresholds.json`. **Posts phải có text link chứa `/ui/`** (không chỉ shortcode) + ít nhất 1 `/visas/`. Visa pages cần `/ui/` + `/posts/`. |
| Offers validation | `label` + `disclosure` checked cho banned words. Disclosure phải "clear and conspicuous" (FTC 2025-2026). |

### Bối cảnh SEO 2025-2026 (từ nghiên cứu web)

| Yếu tố | Thực tế | Nguồn |
|---------|---------|-------|
| Helpful Content | Tích hợp vào core updates. AI content không bị phạt nếu có giá trị thực. December 2025 Core Update phạt nặng lazy content (-40-60% traffic). | [Google SEO Updates 2024-2025](https://www.saffronedge.com/blog/google-seo-updates/), [December 2025 Core Update](https://almcorp.com/blog/google-december-2025-core-update-complete-guide/) |
| FAQ Rich Results | Từ 08/2023: chỉ hiển thị cho government/health sites. Schema vẫn nên giữ vì giúp AI/search hiểu content. June 2025: Google drop 7 schema types khác nhưng giữ FAQ. | [Google FAQ Changes](https://developers.google.com/search/blog/2023/08/howto-faq-changes), [FAQ Schema 2025](https://www.epicnotion.com/blog/faq-schema-in-2025/) |
| AI Overviews | ~15-16% queries có AI Overview. CTR organic giảm 61% khi có AIO. Brands được cite thấy +35% CTR. Tối ưu: answer-first, H2/H3 là câu hỏi, fact density cao. | [AI Overviews Guide 2026](https://koanthic.com/en/google-ai-overviews-optimization-complete-guide-2026/), [Google Official Advice](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search) |
| FTC Disclosure | "Clear and conspicuous" — đầu content, trước affiliate links. June 2025: mọi affiliate link = paid endorsement. Phạt đến $51,744/violation. | [FTC Affiliate Disclosure 2026](https://www.referralcandy.com/blog/ftc-affiliate-disclosure), [FTC Guidelines 2025](https://www.heyseva.com/blog-posts/ftc-guidelines-for-affiliates-creators-and-brands-2025) |
| E-E-A-T | "Experience" quan trọng hơn bao giờ hết. First-hand experience > theoretical knowledge. YMYL cần sources chính phủ/đại sứ quán. | [Helpful Content Guidelines](https://www.whitepress.com/en/knowledge-base/2227/google-helpful-content) |
| HowTo Schema | Không còn rich results (dropped 08/2023). Không cần triển khai. | [Google HowTo/FAQ Changes](https://developers.google.com/search/blog/2023/08/howto-faq-changes) |

---

## Dữ liệu hiện có — Inventory

| Loại | Số lượng | Chi tiết |
|------|----------|----------|
| Visa routes | 6 | ES_DNV, PT_DNV, DE_FREELANCE, MT_NOMAD, CR_DN, TH_DTV |
| Products | 7 active | ASISA, DKV, Genki, SafetyWing, Sanitas, WorldNomads, GenericInsurer |
| Mappings | 42 | 6 × 7 combinations |
| Sources | 21 evidence files + 21 meta.json | PDFs, HTML, MD |
| Hub posts | 11 active | 6 route-specific + 3 regional + 1 comparison + 1 trap-related |
| Guides | 2 | how-to-read-results, schengen-30000 |
| Traps | 2 | malta-monthly, spain-mistakes |
| Visa pages | 6 routes × 2 levels | _index.md (generated) + authority/index.md |
| Offers | 2 | Genki (affiliate), ASISA (non-affiliate) |

**Capacity thực tế:** Với 6 visa routes × 7 products, có thể tạo tối đa ~25-30 bài có evidence đầy đủ (6 hub + 6 visa deep-dive + 7 product pages + 3 regional + 2-3 comparison + 2-3 traps + 2-3 guides). **Không khả thi 50 bài** mà không mở rộng data.

---

## Lộ trình 12 Tuần

### Phase 0: Data Foundation (Tuần 1-2)

> **Nguyên tắc:** Không mở rộng content trước khi mở rộng data.

#### Task 1: Audit evidence gaps trong 6 visa routes hiện có

**Files:**
- Read: `data/visas/*/` (tất cả visa_facts.json)
- Read: `sources/*.meta.json` (tất cả evidence metadata)
- Create: `docs/evidence-gap-report.md`

**Step 1: Chạy validate để kiểm tra data integrity**

```bash
py tools/validate.py 2>&1 | tee /tmp/validate-report.txt
```

Expected: List of any missing sources or SHA256 mismatches. Lưu ý: `validate.py` chỉ kiểm tra schema conformance + source tồn tại + SHA256. Nó **không** báo requirement nào thiếu evidence.

**Step 2: Chạy gap audit script để tìm requirements thiếu evidence**

Viết script `tools/audit_evidence_gaps.py` đọc từng `visa_facts.json` và `product_facts.json`, liệt kê mỗi requirement/spec field có hay không có evidence array. Đây là bước bắt buộc vì `validate.py` không thực hiện chức năng này.

```bash
py tools/audit_evidence_gaps.py 2>&1 | tee /tmp/gap-report.txt
```

Script cần:
- Đọc tất cả `data/visas/**/visa_facts.json`
- Cho mỗi requirement, kiểm tra có `evidence` array với ít nhất 1 item hay không
- Đọc tất cả `data/products/**/product_facts.json`
- Cho mỗi spec field, kiểm tra có evidence hay không
- Output: danh sách gaps theo route/product

**Step 3: Tạo evidence gap report**

Tạo file `docs/evidence-gap-report.md` với format:

```markdown
# Evidence Gap Report — YYYY-MM-DD

## Per Visa Route

### ES_DNV_BLS_LONDON_2026
- Total requirements: N
- Requirements with evidence: N
- Missing evidence for: [list fields]
- Sources: [list source_ids]

[repeat for each route]

## Per Product
[same structure]

## Priority Actions
1. [highest-impact gap]
2. ...
```

**Step 4: Commit**

```bash
git add tools/audit_evidence_gaps.py docs/evidence-gap-report.md
git commit -m "docs: add evidence gap audit script and report"
```

---

#### Task 2: Xác định minimum evidence density standard

**Files:**
- Create: `docs/evidence-density-standard.md`

**Step 1: Định nghĩa standard**

```markdown
# Evidence Density Standard

## Minimum Requirements per Content Type

### Hub Post (content/posts/)
- >= 3 evidence items cited (source_id references)
- >= 1 government/consulate source
- >= 1 product_facts reference
- All claims link to snapshot= deep links

### Visa Route Page (content/visas/**/index.md)
- Generated from visa_facts.json — must have >= 2 requirements with evidence
- Each requirement must have source_id + locator

### Trap Page (content/traps/)
- >= 2 evidence items showing the trap scenario
- >= 1 mapping result demonstrating the issue

### Guide Page (content/guides/)
- >= 2 evidence items
- Step-by-step must reference actual tool output

### Comparison Page
- >= 1 evidence item per product compared
- All product claims from product_facts.json
```

**Step 2: Commit**

```bash
git add docs/evidence-density-standard.md
git commit -m "docs: define evidence density standard"
```

---

#### Task 3: Thu thập thêm evidence cho routes thiếu data

**Files:**
- Create: new `sources/*.meta.json` + evidence files cho routes thiếu
- Modify: `data/visas/` và `data/products/` nếu cần thêm requirements

**Step 1: Ưu tiên theo impact**

Thứ tự ưu tiên thu thập evidence:
1. ES (Spain) — thị trường lớn nhất, cạnh tranh cao
2. PT (Portugal) — D8 phổ biến, nhiều traffic tiềm năng
3. DE (Germany) — freelance visa demand cao
4. TH (Thailand) — DTV mới, ít cạnh tranh
5. CR (Costa Rica) — niche nhỏ
6. MT (Malta) — niche nhỏ

**Step 2: Cho mỗi route, thu thập từ primary sources**

Sources ưu tiên:
- Government/consulate official pages
- VFS Global / BLS / TLS Contact checklists
- Official insurance provider policy documents

**Step 3: Validate mỗi source mới**

```bash
py tools/validate.py --visa data/visas/{COUNTRY}/{TYPE}/{authority}/{date}/visa_facts.json
py tools/validate.py --product data/products/{Provider}/{Product}/{date}/product_facts.json
```

**Step 4: Rebuild mappings + index**

```bash
py tools/build_mappings.py
py tools/build_index.py
```

**Step 5: Commit**

```bash
git add sources/ data/
git commit -m "feat: add evidence for [route] from [source]"
```

> **Gate (Option B):** Route được vào Phase 1 nếu **(a)** có >= 2 requirements with evidence **hoặc** **(b)** visa có `insurance_not_required = true` **hoặc** **(c)** chỉ có 1 requirement nhưng evidence đầy đủ từ primary source.

---

### Phase 1: Nâng chất Hub Posts hiện có (Tuần 3-5)

> **Nguyên tắc:** Cải thiện content đã indexed trước khi tạo content mới. Compound growth.

#### Task 4: Nâng cấp hub posts route-specific (ưu tiên theo evidence depth)

**Files:**
- Modify (Phase 1 start): `content/posts/spain-dnv-insurance/index.md`
- Modify (Phase 1 start): `content/posts/germany-freelance-insurance.md`
- Modify (Phase 1 start): `content/posts/malta-nomad-insurance.md`
- Modify (Phase 1 start): `content/posts/costa-rica-dn-insurance.md`
- Modify (Phase 1 start): `content/posts/thailand-dtv-insurance.md`
- Modify (Phase 1 later, after extra PT requirements): `content/posts/portugal-dnv-insurance.md`
- Modify: `tools/seo_thresholds.json` (cập nhật word count nếu cần)

**Step 1: Ưu tiên theo evidence depth**

Phase 1 start (đủ >=2 requirements hoặc NOT_REQUIRED): ES, DE, MT, CR, TH.

Portugal: chỉ có 1 requirement (insurance.mandatory). **Trì hoãn** cho đến khi bổ sung thêm requirements (min_coverage, no_deductible, full_period, monthly_payments_accepted) từ primary sources.

**Step 2: Cho mỗi hub post, thêm/cải thiện các block sau**

Checklist per post:
- [ ] "What the authority requires" — thêm evidence citations mới
- [ ] "How we evaluate" — link đến methodology
- [ ] "Check in the engine" — CTA với deep link `snapshot=` mới nhất
- [ ] FAQ frontmatter — thêm 2-3 câu hỏi thực tế (answer-first cho AI Overviews)
- [ ] "Disclaimer" — clear, top-level
- [ ] "Affiliate disclosure" — "clear and conspicuous", trước affiliate links (FTC 2025-2026)
- [ ] Internal links: `/ui/` + `/visas/` (SEO audit requirement)
- [ ] Không chứa banned words

**Step 3: Tối ưu cho AI Overviews**

Cho mỗi post:
- H2/H3 dạng câu hỏi (ví dụ: "## What insurance does Spain require for a digital nomad visa?")
- Đoạn mở đầu sau H2: trả lời trực tiếp trong 1-2 câu (answer-first)
- Bullet points cho requirements list
- Fact density cao: mỗi paragraph có >= 1 evidence reference

**Step 4: Validate từng post**

```bash
py tools/lint_content.py content/posts/{file}
py tools/seo_audit.py
```

Expected: PASS cho cả lint và SEO audit.

**Step 5: Commit từng post**

```bash
git add content/posts/{file}
git commit -m "docs: deepen {route} hub post with evidence + FAQ"
```

---

#### Task 5: Nâng cấp 3 regional hub posts

**Files:**
- Modify: `content/posts/digital-nomad-insurance-europe.md`
- Modify: `content/posts/digital-nomad-insurance-asia.md`
- Modify: `content/posts/digital-nomad-insurance-americas.md`

**Step 1: Thêm spoke links đến route-specific posts**

Mỗi regional post phải link đến tất cả route posts trong region đó:
- Europe: Spain, Portugal, Germany, Malta
- Asia: Thailand
- Americas: Costa Rica

**Step 2: Thêm comparison table từ mapping data**

Bảng so sánh "Route × Top Product → Status" cho mỗi region. Dữ liệu lấy từ `data/mappings/`. Không suy đoán — chỉ dùng mapping status thực (GREEN/YELLOW/RED/UNKNOWN).

**Step 3: Validate + Commit**

```bash
py tools/lint_content.py content/posts/digital-nomad-insurance-europe.md
py tools/lint_content.py content/posts/digital-nomad-insurance-asia.md
py tools/lint_content.py content/posts/digital-nomad-insurance-americas.md
py tools/seo_audit.py
git add content/posts/digital-nomad-insurance-*.md
git commit -m "docs: add spoke links + mapping tables to regional hubs"
```

---

#### Task 6: Nâng cấp comparison post

**Files:**
- Modify: `content/posts/safetywing-vs-worldnomads-vs-genki.md`

**Step 1: Thêm evidence-based comparison table**

Bảng so sánh 3 products dựa trên product_facts.json:
- `specs.overall_limit`
- `specs.deductible.amount`
- `specs.copay`
- `specs.payment_cadence`
- Mapping status cho mỗi visa route

Mỗi cell phải có source_id reference. Nếu thiếu data → ghi "UNKNOWN (chưa xác minh)".

**Step 2: FTC-compliant disclosure**

Thêm disclosure block ở đầu bài (trước bất kỳ affiliate link nào):

```markdown
> **Affiliate disclosure:** Some links on this page are affiliate links. We may earn a commission if you purchase through these links. This does not affect our compliance evaluation, which is automated and evidence-based. See our [methodology](/guides/how-to-read-results/).
```

**Step 3: Validate + Commit**

```bash
py tools/lint_content.py content/posts/safetywing-vs-worldnomads-vs-genki.md
py tools/seo_audit.py
git add content/posts/safetywing-vs-worldnomads-vs-genki.md
git commit -m "docs: evidence-based comparison table + FTC disclosure"
```

---

### Phase 2: Content mới có chọn lọc (Tuần 6-9)

> **Nguyên tắc:** Chỉ tạo content mới khi có đủ evidence. Mỗi bài phải pass pipeline.

#### Task 7: Tạo 2-3 trap pages mới (nếu có evidence)

**Files:**
- Create: `content/traps/{new-trap}.md`
- Modify: `seo_thresholds.json` (thêm word count)

**Step 1: Xác định trap scenarios từ mapping data**

Quét `data/mappings/` tìm patterns:
- Products có RED status trên nhiều routes → trap phổ biến
- Products có UNKNOWN → thiếu thông tin, cảnh báo người dùng

Ví dụ traps tiềm năng:
- "Deductible trap: nhiều travel insurance có deductible > 0 bị reject ở Spain/Portugal"
- "Monthly payment trap: subscription plans bị reject khi visa yêu cầu full-period"

**Step 2: Viết trap page theo template**

Mỗi trap page phải có 5 required blocks + evidence references + `snapshot=` deep links.

```markdown
---
title: "[Trap name] — evidence-based warning"
date: YYYY-MM-DD
tags: ["trap", "{country}", "compliance"]
---

> **Affiliate disclosure:** [clear, conspicuous, trước mọi link]

## What the authority requires
[Evidence from visa_facts.json]

## The trap
[Mapping data showing RED/UNKNOWN]

## How we evaluate
[Reference to rule engine logic]

## How to avoid this
[Evidence-based recommendation — NO banned words]

## Check in the engine
[Deep link with snapshot=]

## Disclaimer
[Standard disclaimer]
```

**Step 3: Validate + Commit**

```bash
py tools/lint_content.py content/traps/{file}
py tools/seo_audit.py
git add content/traps/{file} seo_thresholds.json
git commit -m "docs: add trap page for {scenario}"
```

---

#### Task 8: Tạo 1-2 guide pages mới

**Files:**
- Create: `content/guides/{new-guide}.md`
- Modify: `seo_thresholds.json`

**Step 1: Guide topics ưu tiên (intent-based)**

Chỉ tạo guide khi có đủ data:
1. "How to choose travel insurance for a digital nomad visa" — dùng mapping data để show decision tree
2. "Understanding compliance statuses: GREEN, YELLOW, RED, UNKNOWN" — explain engine output

**Step 2: Viết theo required blocks + answer-first cho AI Overviews**

H2 dạng câu hỏi, câu trả lời mở đầu, evidence citations.

**Step 3: Validate + Commit**

```bash
py tools/lint_content.py content/guides/{file}
py tools/seo_audit.py
git add content/guides/{file} seo_thresholds.json
git commit -m "docs: add guide for {topic}"
```

---

#### Task 9: Thêm offers cho products còn thiếu

**Files:**
- Modify: `data/offers/offers.json`

**Step 1: Xác định products chưa có offer**

Hiện có: Genki (affiliate), ASISA (non-affiliate). Còn thiếu: DKV, SafetyWing, Sanitas, WorldNomads. **Generic placeholder (GENERIC_EXPAT_COMPLETE_2026) — skip.**

**Step 2: Thêm offers (non-affiliate nếu chưa có partnership)**

> **Lưu ý schema:** `affiliate_url`, `label`, `disclosure` đều **bắt buộc**.  
> Với non-affiliate, dùng official link làm `affiliate_url`.

```json
{
  "product_id": "SAFETYWING_NOMAD_2026",
  "affiliate_url": "https://safetywing.com/nomad-insurance",
  "label": "View SafetyWing Nomad Insurance",
  "disclosure": "Paid link. We may earn a commission if you purchase through this link."
}
```

Hoặc nếu chưa có affiliate deal (vẫn đủ 4 fields theo schema):
```json
{
  "product_id": "DKV_VISADO_2026",
  "affiliate_url": "https://dkv.es/particulares/seguros-salud-extranjeros",
  "label": "View DKV Visado (official)",
  "disclosure": "Official link (non-affiliate). We do not earn a commission."
}
```

**Step 3: Validate offers**

```bash
py tools/validate.py
```

Expected: offers pass banned words check.

**Step 4: Rebuild index + Commit**

```bash
py tools/build_index.py
git add data/offers/offers.json data/ui_index.json
git commit -m "feat: add offers for additional products"
```

---

### Phase 3: Technical SEO + Distribution (Tuần 10-12)

#### Task 10: Internal linking audit

**Files:**
- Modify: all content files to ensure cross-linking

**Step 1: Chạy SEO audit để tìm missing links**

```bash
py tools/seo_audit.py 2>&1 | tee /tmp/seo-audit.txt
```

**Step 2: Fix tất cả link violations**

SEO thresholds yêu cầu:
- `content/posts/*.md` → phải có `/ui/` + ít nhất 1 `/visas/`
- `content/visas/**/index.md` → phải có `/ui/` + ít nhất 1 `/posts/`

**Step 3: Validate + Commit**

```bash
py tools/seo_audit.py
py tools/lint_content.py
git add content/
git commit -m "fix: resolve internal linking gaps from SEO audit"
```

---

#### Task 11: FAQ frontmatter expansion

**Files:**
- Modify: content files listed in `seo_thresholds.json` → `require_faq`

**Step 1: Cho mỗi file trong require_faq list, đảm bảo có FAQ frontmatter**

FAQ phải:
- Câu hỏi phản ánh real user queries (intent-based)
- Câu trả lời answer-first, ngắn gọn, có evidence reference
- Không chứa banned words

**Step 2: FAQ tối ưu cho AI Overviews**

Mỗi answer nên:
- Bắt đầu bằng câu trả lời trực tiếp
- Ngắn (2-3 câu)
- Chứa entity cụ thể (tên nước, tên product, số tiền coverage)

**Step 3: Validate + Commit**

```bash
py tools/lint_content.py
py tools/seo_audit.py
git add content/
git commit -m "docs: expand FAQ frontmatter for AI Overview optimization"
```

---

#### Task 12: Snapshot + Release

**Files:**
- Run: `tools/build_snapshot.py`
- Run: `tools/build_release_snapshot.py`

**Step 1: Tạo snapshot**

```bash
py tools/build_snapshot.py
```

**Step 2: Tạo release snapshot**

```bash
py tools/build_release_snapshot.py --release-id 2026-02-XX
```

**Step 3: Sync Hugo static**

```bash
py tools/sync_hugo_static.py
```

**Step 4: Build Hugo**

```bash
hugo
```

Expected: Build success, no errors.

**Step 5: Verify build + Tag**

> **Lưu ý:** `static/` và `data/snapshots/` là generated artifacts — **KHÔNG commit** theo guideline repo (CLAUDE.md). Chỉ chạy snapshot + sync để build local/CI.

```bash
# Verify build output exists (do NOT git add these)
ls data/snapshots/
ls static/

# Tag the release on current commit (content + data changes already committed)
git tag v2026-02-XX
```

---

## KPI Framework

### Đo lường (tương thích GTM hiện có)

| KPI | Event trong GTM | Mục tiêu 12 tuần |
|-----|-----------------|-------------------|
| Outbound Affiliate Click Rate (OACR) | `click_affiliate` / `run_check` | Tăng 20% so với baseline |
| Engaged Check Rate | `run_check` / page_view | Tăng 15% |
| Evidence View Rate | `open_evidence` / `run_check` | > 10% (trust signal) |
| Copy Link Rate | `copy_link` / `run_check` | > 5% (share signal) |
| Organic CTR (Search Console) | N/A (external) | Monitor, không set target chưa có baseline |

### Không A/B test — thay bằng observational optimization

Với traffic thấp ban đầu, A/B test thiếu statistical power. Thay vào đó:
- **Tuần 4:** So sánh OACR trước/sau Phase 1 (pre-post, không concurrent)
- **Tuần 8:** So sánh engagement metrics trước/sau Phase 2
- **Tuần 12:** Tổng kết, quyết định có scale Phase 3+ hay không

---

## Scope Không Làm (Explicit Exclusions)

| Yêu cầu gốc | Lý do loại bỏ |
|--------------|---------------|
| 50 bài (20 money + 30 supporting) | Chỉ có data cho ~25-30 bài tối đa. Viết thêm = padding hoặc vi phạm evidence-first. |
| Mini-checker (Yes/No questionnaire) | Cần thiết kế product + code UI mới. Không khả thi trong 12 tuần song song với content. Đưa vào backlog riêng. |
| 500 từ tối thiểu cho mọi trang | Thay bằng evidence density standard. Nhiều visa routes chỉ có 3-5 requirements — 500 từ = padding. |
| Screenshot toàn trang khi update | Pipeline chỉ snapshot JSON + manifest SHA256. Screenshot cần Playwright pipeline riêng. Nếu cần hình → snippet nhỏ + citation. |
| 8 A/B tests | Traffic không đủ sample size. Thay bằng pre-post observational. |
| HowTo schema | Google đã drop HowTo rich results (08/2023). Không triển khai. |
| 150-300 từ khóa | Với 6 routes, focus ~30-50 từ khóa thực tế. |

---

## Roadmap mở rộng Data (sau 12 tuần)

Nếu Phase 0-3 thành công:

### Phase 4 (Tuần 13-18): Thêm 4-6 visa routes mới
- Ưu tiên: Italy (Elective Residence), Czech Republic (Zivno), Colombia (Digital Nomad), UAE (Remote Work)
- Mỗi route cần: visa_facts.json + >= 2 primary sources + product mappings

### Phase 5 (Tuần 19-24): Thêm 3-5 products mới
- Ưu tiên: products phổ biến trong digital nomad communities
- Mỗi product cần: product_facts.json + evidence files + SHA256 validation

### Phase 6 (Tuần 25+): Mini-checker feature
- Thiết kế product specification
- UI/JS development
- Test against existing mapping data
- Chỉ bắt đầu khi có >= 12 routes + 10 products

---

## Verification Checklist

Trước khi ship bất kỳ content nào:

```bash
# 1. Validate data integrity
py tools/validate.py

# 2. Lint content blocks + banned words
py tools/lint_content.py

# 3. SEO audit (word count, links, FAQ)
py tools/seo_audit.py

# 4. Rebuild mappings + index
py tools/build_mappings.py
py tools/build_index.py

# 5. Hugo build
hugo

# 6. Run tests
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
powershell -NoProfile -File tools/tests/validate_product_sources_tests.ps1
```

Tất cả phải PASS. Nếu bất kỳ bước nào FAIL → fix trước khi commit.
