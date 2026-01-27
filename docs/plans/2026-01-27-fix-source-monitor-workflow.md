# Source Monitor Workflow Fix Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix the `.github/workflows/source-monitor-pr.yml` parse failure so the workflow can run again.

**Architecture:** Adjust the inline Python snippet to keep the `out.write(...)` on a single, properly indented line in the YAML block. This resolves YAML parsing and keeps the output format unchanged.

**Tech Stack:** GitHub Actions YAML, inline Python

---

### Task 1: Confirm current workflow error line

**Files:**
- Modify: `.github/workflows/source-monitor-pr.yml`

**Step 1: Locate the broken line**

Run: `rg -n "out.write\\(f\\\"changed" .github/workflows/source-monitor-pr.yml`
Expected: Shows the `out.write(...)` split across two lines (broken).

**Step 2: Commit (placeholder)**

No commit in this task.

---

### Task 2: Fix YAML/Python line and verify

**Files:**
- Modify: `.github/workflows/source-monitor-pr.yml`

**Step 1: Write the minimal fix**

Change the output line to a single, indented line:

```yaml
          with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as out:
              out.write(f"changed={str(changed).lower()}\\n")
```

**Step 2: Verify line is intact**

Run: `rg -n "out.write\\(f\\\"changed=.*\\\\n\\\"\\)" .github/workflows/source-monitor-pr.yml`
Expected: One line match.

**Step 3: Commit**

```bash
git add .github/workflows/source-monitor-pr.yml
git commit -m "fix: repair source monitor workflow output line"
```

