# Workspace Hygiene Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Clean the repository state without changing production behavior by removing stale artifacts, fixing .gitignore gaps, deleting `KQ.md`, and aligning generated files with source‑of‑truth.

**Architecture:** Perform cleanup in the current (dirty) workspace so files are visible. Use gitignore rules to suppress local artifacts, untrack previously‑committed generated files (`static/*`), restore accidental edits, and fix a flaky test that dirties fixtures. Clean worktrees/remote branches last.

**Tech Stack:** Git, PowerShell (tests), Python build tools, Hugo.

---

### Task 0: Create a cleanup branch in the current workspace

**Files:**
- Create: (none)
- Modify: (none)
- Test: (manual)

**Step 1: Write the failing test**  
Run: `git status -s`  
Expected: output shows dirty workspace (cleanup must run here).

**Step 2: Run test to verify it fails**  
Run: `git branch --show-current`  
Expected: on `main` or another non‑cleanup branch.

**Step 3: Write minimal implementation**  
Run: `git checkout -b chore/workspace-hygiene`

**Step 4: Run test to verify it passes**  
Run: `git branch --show-current`  
Expected: `chore/workspace-hygiene`.

**Step 5: Commit**  
No commit for this task.

---

### Task 1: Delete `KQ.md` permanently (user confirmed)

**Files:**
- Delete: `KQ.md`
- Modify: (none)
- Test: (manual)

**Step 1: Write the failing test**  
Run: `git status -s | rg "KQ.md"`  
Expected: shows `D KQ.md`.

**Step 2: Run test to verify it fails**  
Run: `test -f KQ.md`  
Expected: non‑zero exit (file already deleted in working tree).

**Step 3: Write minimal implementation**  
Run: `git rm KQ.md`

**Step 4: Run test to verify it passes**  
Run: `git status -s | rg "KQ.md"`  
Expected: shows `D KQ.md` staged for commit.

**Step 5: Commit**  
Run:
```bash
git commit -m "docs: remove KQ report"
```

---

### Task 2: Add missing `.gitignore` entries (local artifacts)

**Files:**
- Modify: `.gitignore`
- Test: (manual)

**Step 1: Write the failing test**  
Run: `git check-ignore -v .bin/ .trae/ context.db data/snapshots/`  
Expected: no output (not ignored).

**Step 2: Run test to verify it fails**  
Run: `rg -n "data/snapshots|context.db|\\.bin|\\.trae" .gitignore`  
Expected: no matches.

**Step 3: Write minimal implementation**  
Add to `.gitignore`:
```
.bin/
.trae/
context.db*
data/snapshots/
```
**Note:** keep `docs/plans/` tracked (do not ignore).

**Step 4: Run test to verify it passes**  
Run: `git check-ignore -v .bin/ .trae/ context.db data/snapshots/`  
Expected: shows ignore rules.

**Step 5: Commit**  
Run:
```bash
git add .gitignore
git commit -m "chore: ignore local workspace artifacts"
```

---

### Task 2b: Commit plan documents (keep tracked)

**Files:**
- Add: `docs/plans/2026-01-24-ux-seo-accessibility-optimization.md`
- Add: `docs/plans/2026-01-24-visa-content-hubs-implementation.md`
- Add: `docs/plans/2026-01-26-seo-tech-content-hardening.md`
- Add: `docs/plans/2026-01-26-workspace-hygiene-cleanup.md`

**Step 1: Write the failing test**  
Run: `git status -s | rg "^\\?\\? docs/plans/"`  
Expected: shows plan files as untracked.

**Step 2: Run test to verify it fails**  
Run: `ls docs/plans`  
Expected: files exist locally but are untracked.

**Step 3: Write minimal implementation**  
Run:
```bash
git add docs/plans/*.md
```

**Step 4: Run test to verify it passes**  
Run: `git status -s | rg "docs/plans"`  
Expected: plan files are staged, not untracked.

**Step 5: Commit**  
Run:
```bash
git commit -m "docs: add cleanup and planning notes"
```

---

### Task 3: Restore unintentional edits in generated outputs & fixtures (non-static)

**Files:**
- Restore: `data/ui_index.json`
- Restore: `tools/tests/fixtures/source_monitor/fixtures/TEST_SOURCE.txt`
- Restore: `tools/tests/fixtures/source_monitor/sources/TEST_SOURCE.meta.json`
- Test: (manual)

**Step 1: Write the failing test**  
Run: `git status -s | rg "data/ui_index.json|TEST_SOURCE"`  
Expected: shows these files as modified.

**Step 2: Run test to verify it fails**  
Run: `git diff --name-only | rg "data/ui_index.json|TEST_SOURCE"`  
Expected: lists these files.

**Step 3: Write minimal implementation**  
Run:
```bash
git restore data/ui_index.json \
  tools/tests/fixtures/source_monitor/fixtures/TEST_SOURCE.txt \
  tools/tests/fixtures/source_monitor/sources/TEST_SOURCE.meta.json
```

**Step 4: Run test to verify it passes**  
Run: `git status -s | rg "data/ui_index.json|TEST_SOURCE"`  
Expected: no output for these paths.

**Step 5: Commit**  
If no changes remain, skip commit. If any remain intentionally, commit with a clear message.

---

### Task 4: Fix source_monitor test to avoid dirty fixtures

**Files:**
- Modify: `tools/tests/source_monitor_tests.ps1`
- Test: `tools/tests/source_monitor_tests.ps1`

**Step 1: Write the failing test**  
Run: `pwsh -NoProfile -File tools/tests/source_monitor_tests.ps1`  
Expected: test passes but leaves fixtures dirty (current behavior).

**Step 2: Run test to verify it fails**  
Run: `git status -s | rg "TEST_SOURCE"`  
Expected: fixtures become modified (fails cleanliness check).

**Step 3: Write minimal implementation**  
Edit `tools/tests/source_monitor_tests.ps1` to add `-NoNewline`:
```powershell
Set-Content -Path $fixturePath -Value $originalFixture -NoNewline
Set-Content -Path $metaPath -Value $originalMeta -NoNewline
```

**Step 4: Run test to verify it passes**  
Run: `pwsh -NoProfile -File tools/tests/source_monitor_tests.ps1`  
Expected: PASS.  
Run: `git status -s | rg "TEST_SOURCE"`  
Expected: no output.

**Step 5: Commit**  
Run:
```bash
git add tools/tests/source_monitor_tests.ps1
git commit -m "test: prevent source monitor fixtures from changing"
```

---

### Task 5: Untrack generated static artifacts already in git

**Files:**
- Modify (index only): `static/ui/`, `static/data/`, `static/snapshots/`
- Test: (manual)

**Step 1: Write the failing test**  
Run: `git ls-files static/ui static/data static/snapshots`  
Expected: lists files (tracked).

**Step 2: Run test to verify it fails**  
Run: `git status -s | rg "^M static/"`  
Expected: shows modified tracked static files.

**Step 3: Write minimal implementation**  
Run:
```bash
git rm --cached -r static/ui static/data static/snapshots
```

**Step 4: Run test to verify it passes**  
Run: `git ls-files static/ui static/data static/snapshots`  
Expected: no output.

**Step 5: Commit**  
Run:
```bash
git add -u
git commit -m "chore: stop tracking generated static assets"
```

---

### Task 6: Restore `faq:` front matter removals in visa pages

**Files:**
- Restore: `content/visas/**/index.md` (6 files)
- Test: (manual)

**Step 1: Write the failing test**  
Run: `rg -n \"^faq:\" content/visas -g\"index.md\"`  
Expected: missing `faq:` blocks (fails if we expect FAQ to exist).

**Step 2: Run test to verify it fails**  
Run: `git status -s | rg \"content/visas/\"`  
Expected: shows 6 files modified.

**Step 3: Write minimal implementation**  
Decision (required): **restore FAQ blocks** to preserve FAQPage schema.  
Run:
```bash
git restore content/visas/costa-rica/digital-nomad-visa/executive-decree-43619/index.md \
  content/visas/germany/freelance-visa-national-d/embassy-london/index.md \
  content/visas/malta/nomad-residence-permit/residency-malta-agency/index.md \
  content/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/index.md \
  content/visas/spain/digital-nomad-visa/consulate-via-bls-london/index.md \
  content/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/index.md
```

**Step 4: Run test to verify it passes**  
Run: `rg -n \"^faq:\" content/visas -g\"index.md\"`  
Expected: `faq:` blocks present.

**Step 5: Commit**  
No commit if restored (matches HEAD).

---

### Task 7: Remove untracked local artifacts (after .gitignore)

**Files:**
- Delete (local): `.bin/`, `data/snapshots/`
- Test: (manual)

**Step 1: Write the failing test**  
Run: `git status -s | rg \"^\\?\\?\"`  
Expected: shows untracked items.

**Step 2: Run test to verify it fails**  
Run: `ls .bin data/snapshots 2>/dev/null`  
Expected: shows files/dirs if present.

**Step 3: Write minimal implementation**  
Run:
```bash
rm -rf .bin data/snapshots
```

**Step 4: Run test to verify it passes**  
Run: `git status -s | rg \"^\\?\\?\"`  
Expected: no untracked local artifacts (except deliberate working docs).

**Step 5: Commit**  
No commit for this task.

---

### Task 8: Clean stale worktrees

**Files:**
- Delete (local): worktrees under `.worktrees/`
- Test: (manual)

**Step 1: Write the failing test**  
Run: `git worktree list --porcelain`  
Expected: shows stale worktrees.

**Step 2: Run test to verify it fails**  
Run: `ls .worktrees/`  
Expected: lists worktree dirs.

**Step 3: Write minimal implementation**  
Run:
```bash
git worktree remove .worktrees/ci-hugo-order
git worktree remove .worktrees/verify-pr29
git worktree remove --force .worktrees/merge-main
git worktree remove .worktrees/visa-content-hubs
```

**Step 4: Run test to verify it passes**  
Run: `git worktree list --porcelain`  
Expected: only current worktree remains.

**Step 5: Commit**  
No commit for this task.

---

### Task 9: Clean stale remote branches

**Files:**
- Remote-only cleanup
- Test: (manual)

**Step 1: Write the failing test**  
Run: `git branch -r | rg \"feat/ci-hugo-order|feat/gtm-csp-fix|feat/visa-content-hubs\"`  
Expected: shows stale branches.

**Step 2: Run test to verify it fails**  
Run: `gh pr list --state open --head <branch>`  
Expected: none open for branches you plan to delete.

**Step 3: Write minimal implementation**  
Run:
```bash
git push origin --delete feat/ci-hugo-order
git push origin --delete feat/gtm-csp-fix
git push origin --delete feat/monetization-abc-global
git push origin --delete feat/stability-gates
git push origin --delete feat/visa-content-hubs
git push origin --delete plan/checker-lite-plan
git push origin --delete ui-compliance-checker-5220696865302370531
```

**Step 4: Run test to verify it passes**  
Run: `git branch -r | rg \"feat/ci-hugo-order|feat/gtm-csp-fix|feat/visa-content-hubs\"`  
Expected: no output.  
**Note:** Do NOT delete palette branches with open PRs (#26, #30).  
Palette branches safe to delete only after PR check:
- palette-a11y-improvements-13332551624782379229  
- palette-a11y-improvements-15899652891021356428  
- palette-accessible-modal-14142080314689584209  
- palette-accessible-modal-921596787477803273  
- palette-modal-a11y-1413407418128404709  
- palette-modal-a11y-16739424234319246983  
- palette/modal-accessibility-2053045294290935034  
- palette/modal-accessibility-6895560625621458967

**Step 5: Commit**  
No commit for this task.

---

### Task 10: Final verification (align with pages.yml)

**Files:**
- Test: `tools/tests/*`, Hugo build

**Step 1: Write the failing test**  
Run: `git status -s`  
Expected: no unexpected modifications.

**Step 2: Run test to verify it fails**  
Run: `py tools/validate.py`  
Expected: PASS.

**Step 3: Write minimal implementation**  
Run:
```bash
py tools/validate.py
py tools/build_mappings.py
py tools/build_index.py
py tools/build_snapshot.py
py tools/sync_hugo_static.py
pwsh -NoProfile -File tools/tests/ui_compliance_tests.ps1
pwsh -NoProfile -File tools/tests/validate_product_sources_tests.ps1
pwsh -NoProfile -File tools/tests/snapshot_tests.ps1
pwsh -NoProfile -File tools/tests/snapshot_routing_tests.ps1
pwsh -NoProfile -File tools/tests/release_snapshot_tests.ps1
pwsh -NoProfile -File tools/tests/verify_snapshot_manifest_tests.ps1
pwsh -NoProfile -File tools/tests/offers_tests.ps1
pwsh -NoProfile -File tools/tests/content_lint_tests.ps1
pwsh -NoProfile -File tools/tests/source_monitor_tests.ps1
pwsh -NoProfile -File tools/tests/hugo_integration_tests.ps1
pwsh -NoProfile -File tools/tests/sync_hugo_static_tests.ps1
pwsh -NoProfile -File tools/tests/verify_static_bundle_tests.ps1
pwsh -NoProfile -File tools/tests/headers_tests.ps1
pwsh -NoProfile -File tools/tests/analytics_tests.ps1
pwsh -NoProfile -File tools/tests/smoke_tests.ps1
pwsh -NoProfile -File tools/tests/performance_tests.ps1
pwsh -NoProfile -File tools/tests/hugo_build_log_tests.ps1
hugo --quiet
```

**Step 4: Run test to verify it passes**  
Expected: all commands PASS with exit code 0.

**Step 5: Commit**  
No commit for this task.

---

Plan complete and saved to `docs/plans/2026-01-26-workspace-hygiene-cleanup.md`. Two execution options:

1. Subagent-Driven (this session) — I dispatch a fresh subagent per task, review between tasks, fast iteration  
2. Parallel Session (separate) — Open new session with executing-plans, batch execution with checkpoints

Which approach?
