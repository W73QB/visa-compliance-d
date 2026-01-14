# VisaFact UI Upgrade Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the generic SaaS UI into a distinctive "Digital Notary" design that builds trust and reinforces the VisaFact brand.

**Architecture:** Single-file HTML upgrade (`ui/index.html`) with new typography, color palette, animations, and trust signals. Changes are made incrementally with sync to `static/ui/index.html` after each phase. Keep `ui/index.html` ASCII-only (repo rule) and avoid non-ASCII glyphs in new UI text.

**Tech Stack:** HTML, Tailwind CSS (inline config), Vanilla JS, Google Fonts (DM Serif Display + Satoshi)

**Source Reports:**
- `UI.md` - Functional review (P1/P2 issues)
- `UI2.md` - Frontend Design review (aesthetics)

---

## Phase 1: Quick Wins (P1 Issues)

### Task 1: Update Page Title and Meta Description

**Files:**
- Modify: `ui/index.html:6-10`

**Step 1: Read current head section**

Verify current state:
```html
<title>Modern Compliance Checker</title>
<!-- No meta description -->
```

**Step 2: Update title and add meta description**

Replace lines 6-10 with:
```html
<title>VisaFact - Evidence-Based Visa Insurance Compliance Checker</title>
<meta name="description" content="Check if your insurance meets official visa requirements. Evidence-backed results verified against primary sources. No source = UNKNOWN.">
<meta name="keywords" content="visa insurance, compliance checker, Spain DNV, evidence-based">
<meta property="og:title" content="VisaFact - Visa Insurance Compliance Checker">
<meta property="og:description" content="Evidence-backed compliance checking against official visa requirements.">
```

**Step 3: Verify changes**

Run: `rg "<title>" ui/index.html`
Expected: Line shows "VisaFact - Evidence-Based"

**Step 4: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): update page title and add meta description for SEO"
```

---

### Task 2: Update Typography - Replace Inter with Font Pair

**Files:**
- Modify: `ui/index.html:9` (Google Fonts link)
- Modify: `ui/index.html:34` (Tailwind fontFamily config)
- Modify: `ui/index.html:46` (body style)

**Step 1: Update Google Fonts import**

Replace line 9:
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"/>
```

**Step 2: Update Tailwind font config**

Replace line 34:
```javascript
fontFamily: {
  "display": ["'DM Serif Display'", "Georgia", "serif"],
  "body": ["'Plus Jakarta Sans'", "system-ui", "sans-serif"]
},
```

**Step 3: Update body style**

Replace line 46:
```css
body { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
```

**Step 4: Update body class**

Find line 54, change `font-display` to `font-body`:
```html
<body class="bg-background-light dark:bg-background-dark min-h-screen font-body text-text-primary dark:text-white transition-colors duration-200">
```

**Step 5: Update hero headline to use display font**

Find line 78-80, add `font-display`:
```html
<h1 class="font-display text-3xl md:text-5xl font-normal tracking-tight mb-4 text-text-primary dark:text-white">
  VisaFact Compliance Checker
</h1>
```

**Step 6: Verify fonts load**

Run: `rg "DM Serif Display" ui/index.html`
Expected: Font reference found

**Step 7: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): replace Inter with DM Serif Display + Plus Jakarta Sans font pair"
```

---

### Task 3: Update Color Palette - Navy + Gold Theme

**Files:**
- Modify: `ui/index.html:17-33` (Tailwind colors config)

**Step 1: Replace color definitions**

Replace the colors object (lines 17-33):
```javascript
colors: {
  "primary": "#1e3a5f",
  "primary-hover": "#152a45",
  "accent": "#c9a227",
  "accent-hover": "#b8921f",
  "background-light": "#faf8f5",
  "background-dark": "#0f1419",
  "surface-light": "#ffffff",
  "surface-dark": "#1a232e",
  "border-soft": "#e8e4df",
  "border-dark": "#2d3748",
  "success-green": "#059669",
  "warning-yellow": "#d97706",
  "error-red": "#dc2626",
  "unknown-gray": "#6b7280",
  "info-blue": "#0369a1",
  "text-primary": "#1a1a1a",
  "text-secondary": "#525252"
}
```

**Step 2: Verify color change**

Run: `rg "1e3a5f" ui/index.html`
Expected: Primary color found

**Step 3: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): update color palette to navy + gold theme"
```

---

### Task 4: Add Trust Badge to Hero Section

**Files:**
- Modify: `ui/index.html:77-87` (hero section)

**Step 1: Add trust badge after h1**

Insert after line 80 (after closing `</h1>`):
```html
<div class="inline-flex items-center gap-2 px-4 py-2 bg-accent/10 border border-accent/30 rounded-full mb-4">
  <span class="material-symbols-outlined text-accent text-lg icon-filled">verified</span>
  <span class="text-sm font-semibold text-accent">Evidence-Backed Decisions</span>
</div>
```

**Step 2: Verify badge added**

Run: `rg "Evidence-Backed" ui/index.html`
Expected: Badge text found

**Step 3: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): add trust badge 'Evidence-Backed Decisions' to hero"
```

---

### Task 5: Fix Accessibility - Focus States

**Files:**
- Modify: `ui/index.html:45-51` (style section)

**Step 1: Add focus-visible styles**

Add after line 50 (before closing `</style>`):
```css
/* Accessibility: Focus states */
:focus-visible {
  outline: 2px solid #1e3a5f;
  outline-offset: 2px;
}
button:focus-visible, a:focus-visible, select:focus-visible {
  outline: 2px solid #c9a227;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(201, 162, 39, 0.2);
}
```

**Step 2: Verify styles added**

Run: `rg "focus-visible" ui/index.html`
Expected: Focus styles found

**Step 3: Commit**

```bash
git add ui/index.html
git commit -m "fix(ui): add accessible focus-visible states for keyboard navigation"
```

---

### Task 6: Fix Navigation Links (Replace Placeholders)

**Files:**
- Modify: `ui/index.html:62-68` (nav section)

**Step 1: Update nav links with real URLs**

Replace lines 62-68:
```html
<nav class="hidden md:flex items-center gap-8">
  <a class="text-sm font-medium text-text-primary dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" href="../">Home</a>
  <a class="text-sm font-medium text-text-primary dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" href="../visas/">Visas</a>
  <a class="text-sm font-medium text-text-primary dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" href="../methodology/">Methodology</a>
  <a class="text-sm font-medium text-text-primary dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors" href="../disclaimer/">Disclaimer</a>
</nav>
```

**Step 2: Verify links updated**

Run: `rg 'href="#"' ui/index.html`
Expected: No nav links with href="#"

**Step 3: Commit**

```bash
git add ui/index.html
git commit -m "fix(ui): replace placeholder nav links with real URLs"
```

---

### Task 7: Add Mobile Navigation (Hamburger Menu)

**Files:**
- Modify: `ui/index.html:56-74` (header section)
- Modify: `ui/index.html` (add JS for toggle)

**Step 1: Add hamburger button before nav**

Insert after line 61 (after logo div, before nav):
```html
<button id="mobileMenuBtn" class="md:hidden p-2 text-text-primary dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors" aria-label="Toggle menu">
  <span class="material-symbols-outlined text-2xl">menu</span>
</button>
```

**Step 2: Add mobile menu dropdown**

Insert after the nav closing tag (after line 68):
```html
<div id="mobileMenu" class="hidden md:hidden absolute top-16 left-0 right-0 bg-surface-light dark:bg-surface-dark border-b border-border-soft dark:border-border-dark shadow-lg">
  <div class="flex flex-col p-4 gap-2">
    <a class="px-4 py-3 text-sm font-medium text-text-primary dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors" href="../">Home</a>
    <a class="px-4 py-3 text-sm font-medium text-text-primary dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors" href="../visas/">Visas</a>
    <a class="px-4 py-3 text-sm font-medium text-text-primary dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors" href="../methodology/">Methodology</a>
    <a class="px-4 py-3 text-sm font-medium text-text-primary dark:text-white hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors" href="../disclaimer/">Disclaimer</a>
  </div>
</div>
```

**Step 3: Add JS toggle function**

Add before closing `</script>` tag:
```javascript
// Mobile menu toggle
$("mobileMenuBtn")?.addEventListener("click", () => {
  const menu = $("mobileMenu");
  const btn = $("mobileMenuBtn");
  const isOpen = !menu.classList.contains("hidden");
  menu.classList.toggle("hidden");
  btn.querySelector("span").textContent = isOpen ? "menu" : "close";
});
```

**Step 4: Verify mobile menu added**

Run: `rg "mobileMenuBtn" ui/index.html`
Expected: Button and JS found

**Step 5: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): add hamburger menu for mobile navigation"
```

---

### Task 8: Add Loading State

**Files:**
- Modify: `ui/index.html` (add loading skeleton)
- Modify: `ui/index.html` (update init function)

**Step 1: Add loading skeleton after input card**

Insert after line 128 (after input card closing div):
```html
<!-- Loading skeleton -->
<div id="loadingState" class="max-w-4xl mx-auto mb-12 hidden">
  <div class="flex items-center justify-center gap-3 py-8">
    <div class="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent"></div>
    <span class="text-text-secondary font-medium">Loading compliance data...</span>
  </div>
</div>
```

**Step 2: Update init function to show/hide loading**

Find `async function init()` and update:
```javascript
async function init(){
  $("loadingState").classList.remove("hidden");
  try {
    const res = await fetch(DATA_URL, { cache: "no-store" });
    const raw = await res.json();
    INDEX = normalizeIndex(raw);
    // ... rest of init
  } catch (err) {
    console.error(err);
    $("loadingState").innerHTML = `
      <div class="text-center py-8">
        <span class="material-symbols-outlined text-error-red text-4xl mb-2">error</span>
        <p class="text-error-red font-medium">Failed to load data</p>
        <p class="text-text-secondary text-sm mt-1">Please refresh the page or check your connection.</p>
      </div>
    `;
    return;
  }
  $("loadingState").classList.add("hidden");
```

**Step 3: Verify loading state added**

Run: `rg "loadingState" ui/index.html`
Expected: Loading element found

**Step 4: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): add loading state with spinner and inline error handling"
```

---

### Task 9: Update Copyright Year

**Files:**
- Modify: `ui/index.html:302`

**Step 1: Make copyright dynamic**

Replace line 302:
```html
<p class="text-xs text-text-secondary dark:text-gray-600">&copy; <script>document.write(new Date().getFullYear())</script> VisaFact. All rights reserved.</p>
```

**Step 2: Verify copyright updated**

Run: `rg "getFullYear" ui/index.html`
Expected: Dynamic year found

**Step 3: Commit**

```bash
git add ui/index.html
git commit -m "fix(ui): make copyright year dynamic"
```

---

### Task 10: Sync to Static and Test

**Files:**
- Run: `py tools/sync_hugo_static.py`

**Step 1: Run sync script**

```bash
py tools/sync_hugo_static.py
```

**Step 2: Verify sync completed**

```powershell
Get-FileHash ui/index.html
Get-FileHash static/ui/index.html
```
Expected: Hashes match

**Step 3: Run Hugo server to test**

```bash
hugo server -D
```

**Step 4: Manual verification**

Open browser to http://localhost:1313/ui/ and verify:
- [ ] New fonts load (DM Serif Display headlines)
- [ ] Navy + Gold color scheme visible
- [ ] Trust badge shows in hero
- [ ] Mobile menu works on narrow viewport
- [ ] Focus states visible when tabbing
- [ ] Loading spinner shows briefly on refresh

**Step 5: Run UI compliance checks (ASCII-only, links, etc.)**

```powershell
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
```

**Step 6: Commit sync result**

```bash
git add static/ui/index.html
git commit -m "chore: sync ui to static after Phase 1 updates"
```

---

## Phase 2: Visual Identity

### Task 11: Add Page Load Animations

**Files:**
- Modify: `ui/index.html:45-51` (style section)

**Step 1: Add keyframes and animation classes**

Add to style section:
```css
/* Page load animations */
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-up { animation: fadeSlideUp 0.6s ease-out both; }
.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
.delay-300 { animation-delay: 0.3s; }

/* Result reveal animation */
@keyframes revealUp {
  from { opacity: 0; transform: translateY(30px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.animate-reveal { animation: revealUp 0.5s ease-out both; }

/* Status pulse for GREEN */
@keyframes trustPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.4); }
  50% { box-shadow: 0 0 0 8px rgba(5, 150, 105, 0); }
}
.pulse-success { animation: trustPulse 2s ease-in-out infinite; }
```

**Step 2: Apply animations to hero elements**

Update hero section classes:
```html
<div class="text-center mb-12 animate-fade-up">
```

Update input card:
```html
<div class="max-w-4xl mx-auto ... animate-fade-up delay-100">
```

**Step 3: Update renderResult to add animation class**

In `renderResult()` function, add:
```javascript
$("resultArea").classList.add("animate-reveal");
```

**Step 4: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): add page load and result reveal animations"
```

---

### Task 12: Add Subtle Background Texture

**Files:**
- Modify: `ui/index.html:45-51` (style section)

**Step 1: Add paper texture overlay**

Add to style section:
```css
/* Subtle paper texture */
body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  opacity: 0.03;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noise)'/%3E%3C/svg%3E");
  z-index: -1;
}
.dark body::before { opacity: 0.02; }
```

**Step 2: Verify texture added**

Run: `grep -n "feTurbulence" ui/index.html`
Expected: SVG noise filter found

**Step 3: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): add subtle paper texture overlay for document feel"
```

---

### Task 13: Enhance Status Badges with Stamp Style

**Files:**
- Modify: `ui/index.html` (statusPresentation function)
- Modify: `ui/index.html` (add stamp styles)

**Step 1: Add stamp-style CSS**

Add to style section:
```css
/* Stamp-style status badges */
.stamp-badge {
  position: relative;
  padding: 0.5rem 1rem;
  border: 3px solid currentColor;
  border-radius: 0.25rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  transform: rotate(-2deg);
}
.stamp-badge::before {
  content: "";
  position: absolute;
  inset: -2px;
  border: 1px dashed currentColor;
  border-radius: 0.25rem;
  opacity: 0.5;
}
```

**Step 2: Update status chip rendering**

In `renderResult()`, update the statusChip application:
```javascript
$("statusChip").className = `stamp-badge ${pres.chipClass}`;
if (status === "GREEN") {
  $("statusChip").classList.add("pulse-success");
}
```

**Step 3: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): add stamp-style status badges for visual distinction"
```

---

### Task 14: Add Card Depth and Shadow

**Files:**
- Modify: `ui/index.html` (card classes)

**Step 1: Update input card with enhanced shadow**

Find input card div (around line 90), update class:
```html
<div class="max-w-4xl mx-auto bg-surface-light dark:bg-surface-dark rounded-xl border border-border-soft dark:border-border-dark p-6 md:p-10 mb-12 shadow-lg shadow-black/5 dark:shadow-black/20 hover:shadow-xl transition-shadow duration-300 animate-fade-up delay-100">
```

**Step 2: Update result card with enhanced shadow**

Find result area div (around line 132), update class:
```html
<div class="bg-surface-light dark:bg-surface-dark rounded-2xl border border-border-soft dark:border-border-dark overflow-hidden shadow-xl shadow-black/5 dark:shadow-black/20">
```

**Step 3: Commit**

```bash
git add ui/index.html
git commit -m "feat(ui): enhance card depth with improved shadows"
```

---

### Task 15: Final Sync and Phase 2 Verification

**Files:**
- Run: `py tools/sync_hugo_static.py`

**Step 1: Run sync**

```bash
py tools/sync_hugo_static.py
```

**Step 2: Run Hugo server**

```bash
hugo server -D
```

**Step 3: Verify Phase 2 changes**

Open browser to http://localhost:1313/ui/ and verify:
- [ ] Page elements fade in on load
- [ ] Subtle paper texture visible on background
- [ ] Status badge has stamp-style border
- [ ] Cards have enhanced shadow depth
- [ ] GREEN status pulses gently

**Step 4: Commit Phase 2 sync**

```bash
git add static/ui/index.html
git commit -m "chore: sync ui to static after Phase 2 visual identity updates"
```

---

## Summary Checklist

### Phase 1: Quick Wins (P1 Issues)
- [ ] Task 1: Page title and meta description
- [ ] Task 2: Typography (DM Serif + Plus Jakarta Sans)
- [ ] Task 3: Color palette (Navy + Gold)
- [ ] Task 4: Trust badge in hero
- [ ] Task 5: Focus states for accessibility
- [ ] Task 6: Fix placeholder nav links
- [ ] Task 7: Mobile navigation
- [ ] Task 8: Loading state
- [ ] Task 9: Dynamic copyright year
- [ ] Task 10: Sync and test

### Phase 2: Visual Identity
- [ ] Task 11: Page load animations
- [ ] Task 12: Paper texture overlay
- [ ] Task 13: Stamp-style status badges
- [ ] Task 14: Enhanced card shadows
- [ ] Task 15: Final sync and verification

---

## Phase 3: Production Hardening (Optional, if required)

### Task 16: Replace Tailwind CDN with build pipeline

**Goal:** Remove runtime CDN dependency and generate a versioned CSS bundle.

**Files:**
- Add: `package.json`, `tailwind.config.js`
- Add: `ui/styles.css` (Tailwind entry)
- Modify: `ui/index.html` to link local CSS instead of CDN

**Step 1: Add Tailwind build tooling**

```bash
npm init -y
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

**Step 2: Create Tailwind entry CSS**

```css
/* ui/styles.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Step 3: Build CSS and update HTML**

```bash
npx tailwindcss -i ui/styles.css -o ui/tailwind.css --minify
```

Update `ui/index.html` to remove the CDN script and include:
```html
<link rel="stylesheet" href="./tailwind.css">
```

**Step 4: Verify UI compliance tests**

```powershell
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
```

**Step 5: Commit**

```bash
git add ui/index.html ui/styles.css ui/tailwind.css package.json tailwind.config.js
git commit -m "build(ui): replace Tailwind CDN with local build"
```

---

## Test Commands Reference

```bash
# Validate data
py tools/validate.py

# Build and sync
py tools/build_index.py
py tools/sync_hugo_static.py

# Run local server
hugo server -D

# Run UI tests
powershell -NoProfile -File tools/tests/ui_compliance_tests.ps1
```

---

*Plan created: 2026-01-14*
*Based on: UI.md, UI2.md*
