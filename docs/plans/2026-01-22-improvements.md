# Project Improvements Implementation Plan (Revised v2)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refactor the procedural logic in `build_mappings.py` to a maintainable Strategy pattern and establish a standard frontend build pipeline with Tailwind CSS to replace CDN usage.

**Architecture:**
- Backend: Move `evaluate` logic into a `ComplianceEngine` using a list of `Rule` objects (Strategy Pattern). Each rule (e.g., `MandatoryInsuranceRule`) encapsulates one check. `build_mappings.py` will use this engine.
- Frontend: Initialize `package.json`, install Tailwind CSS and PostCSS, configure `tailwind.config.js` to match current inline config, and create a build script to generate static CSS.

**Tech Stack:** Python 3 (pathlib, json), Node.js, Tailwind CSS v4, PostCSS.

---

## Research Findings (Web Search 2026-01-22)

### Tailwind CSS v4 Best Practices
> [!IMPORTANT]
> Tailwind CSS v4 (released 2025-01-22) uses **CSS-first configuration** via `@theme` directive. The `tailwind.config.js` approach is legacy but still supported.
> 
> New recommended setup:
> - Install `tailwindcss` and `@tailwindcss/postcss`
> - Use `postcss.config.mjs` (not `.js`)
> - Define design tokens in CSS with `@theme { ... }`

**Decision:** Since the project currently uses v3-style config (in HTML), we'll migrate to v3-compatible build first, then optionally upgrade to v4 CSS-first approach later.

### Python Rules Engine Best Practices
Key recommendations:
1. **Granular rules**: Each rule checks ONE thing
2. **Auditability**: Log which rules applied, input data, outcomes
3. **Version control**: Treat rules as living documents
4. **Testability**: Each rule independently testable
5. **Error handling**: Consistent error messages for violations

### Hugo + Tailwind Integration
Recommended approach:
1. Place CSS in `assets/css/` for Hugo Pipes processing
2. Use `npm-run-all` for concurrent dev server (Hugo + Tailwind watch)
3. Hugo extended version recommended for PostCSS support
4. Content paths in tailwind.config: `["./layouts/**/*.html", "./content/**/*.md"]`

---

## User Review Required

> [!IMPORTANT]
> **Tailwind Version Choice:** Should we use Tailwind v3 (stable, current plan) or upgrade to v4 CSS-first approach?

> [!WARNING]
> The frontend change will require running `npm run build:css` before every deploy. Consider adding this to CI/CD workflow or Hugo build script.

---

## Task 1: Initialize Frontend Build System

**Files:**
- Create: `package.json`
- Create: `postcss.config.js`
- Create: `tailwind.config.js`
- Create: `assets/css/input.css` (Hugo-compatible location)
- Modify: `ui/index.html`
- Modify: `.gitignore`

### Step 1: Check for existing package.json

Run: `ls -la package.json`
Expected: File not found (proceed to create)

### Step 2: Initialize npm and install dependencies

Run:
```bash
npm init -y
npm install -D tailwindcss postcss autoprefixer npm-run-all
```

Note: `npm-run-all` allows running Hugo and Tailwind watch concurrently.

### Step 3: Configure PostCSS

Create `postcss.config.js`:
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### Step 4: Create Tailwind Config

Create `tailwind.config.js` (extract from `ui/index.html` lines 35-69):
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./ui/**/*.{html,js}",
    "./layouts/**/*.html",
    "./content/**/*.md"
  ],
  darkMode: "class",
  theme: {
    extend: {
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
      },
      fontFamily: {
        "display": ["'DM Serif Display'", "Georgia", "serif"],
        "body": ["'Plus Jakarta Sans'", "system-ui", "sans-serif"]
      },
      borderRadius: {
        "DEFAULT": "0.5rem",
        "lg": "1rem",
        "xl": "1.5rem",
      },
    },
  },
  plugins: [],
}
```

### Step 5: Create Input CSS (CRITICAL: include ALL custom styles)

Create `assets/css/input.css` - must include all custom styles from `ui/index.html` lines 72-143:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  }
}

/* Material Icons settings */
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24;
}
.icon-filled {
  font-variation-settings: 'FILL' 1,'wght' 400,'GRAD' 0,'opsz' 24;
}

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
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  z-index: -1;
}
.dark body::before { opacity: 0.02; }

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

### Step 6: Add build scripts to package.json

Modify `package.json` scripts section:
```json
"scripts": {
  "build:css": "tailwindcss -i ./assets/css/input.css -o ./ui/style.css --minify",
  "watch:css": "tailwindcss -i ./assets/css/input.css -o ./ui/style.css --watch",
  "dev": "npm-run-all --parallel watch:css hugo:dev",
  "hugo:dev": "hugo server -D",
  "build": "npm run build:css && hugo --minify"
}
```

### Step 7: Update .gitignore

Add to `.gitignore`:
```
node_modules/
ui/style.css
```

### Step 8: Build CSS and verify

Run: `npm run build:css`
Expected: `ui/style.css` created, minified.

### Step 9: Update HTML

Modify `ui/index.html`:
1. **Remove** line 30: `<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>`
2. **Remove** lines 34-70: `<script id="tailwind-config">...</script>`
3. **Remove** lines 72-144: `<style>...</style>`
4. **Add** after line 32 (fonts): `<link href="./style.css" rel="stylesheet">`

### Step 10: Verify UI

Run: `python3 -m http.server 8000 --directory .`
Open: `http://localhost:8000/ui/index.html`
Expected: UI looks identical to before (colors, fonts, animations, dark mode all work).

---

## Task 2: Refactor Python Engine (Following Best Practices)

Based on research, key improvements:
1. **Granular rules**: Each rule checks ONE requirement
2. **Auditability**: Return which rule matched, with evidence
3. **Testability**: Each rule is a separate module with its own tests

**Files:**
- Create: `tools/__init__.py` (empty, required for package)
- Create: `tools/rules/__init__.py`
- Create: `tools/rules/base.py`
- Create: `tools/rules/mandatory.py`
- Create: `tools/rules/deductible.py`
- Create: `tools/rules/copayment.py`
- Create: `tools/rules/moratorium.py`
- Create: `tools/rules/coverage.py`
- Create: `tools/rules/jurisdiction.py`
- Create: `tools/rules/payment.py`
- Create: `tools/engine.py`
- Modify: `tools/build_mappings.py`
- Create: `tools/tests/test_rules.py`

### Step 1: Create package structure

Run:
```bash
touch tools/__init__.py
mkdir -p tools/rules
touch tools/rules/__init__.py
```

### Step 2: Create base module with helpers

Create `tools/rules/base.py`:
```python
"""Base classes and utilities for compliance rules."""
from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict

class RuleResult:
    """Structured result from a rule check."""
    def __init__(
        self,
        status: str = "GREEN",
        reasons: Optional[List[Dict]] = None,
        missing: Optional[List[str]] = None,
        terminal: bool = False
    ):
        self.status = status
        self.reasons = reasons or []
        self.missing = missing or []
        self.terminal = terminal  # If True, stop processing other rules

class Rule(ABC):
    """Base class for compliance rules."""
    
    # Human-readable name for audit logs
    name: str = "BaseRule"
    
    @abstractmethod
    def check(self, visa: dict, product: dict) -> Optional[RuleResult]:
        """
        Check if visa/product combination passes this rule.
        
        Returns:
            None if rule doesn't apply (requirement not present).
            RuleResult with status, reasons, missing fields.
        """
        pass

def get_req(visa: dict, key: str) -> Optional[dict]:
    """Get requirement by key from visa."""
    for r in visa.get("requirements", []):
        if r["key"] == key:
            return r
    return None

def product_spec(product: dict, path: str) -> Any:
    """Navigate nested product specs by dot-separated path."""
    cur = product.get("specs")
    for p in path.split("."):
        if cur is None or not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur
```

### Step 3: Create individual rule modules

Create `tools/rules/mandatory.py`:
```python
"""Rule: Check if insurance is mandatory for the visa."""
from tools.rules.base import Rule, RuleResult, get_req

class MandatoryInsuranceRule(Rule):
    name = "MandatoryInsurance"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.mandatory")
        if req and req["value"] is False:
            return RuleResult(
                status="NOT_REQUIRED",
                reasons=[{
                    "text": "Visa does not require insurance",
                    "evidence": req["evidence"]
                }],
                terminal=True
            )
        return None
```

Create `tools/rules/deductible.py`:
```python
"""Rule: Check no deductible requirement."""
from tools.rules.base import Rule, RuleResult, get_req, product_spec

class NoDeductibleRule(Rule):
    name = "NoDeductible"
    
    def check(self, visa, product):
        req = get_req(visa, "insurance.no_deductible")
        if not req or req["value"] is not True:
            return None
        
        ded = product_spec(product, "deductible.amount")
        if ded is None:
            return RuleResult(
                status="UNKNOWN",
                missing=["specs.deductible.amount"]
            )
        if ded > 0:
            return RuleResult(
                status="RED",
                reasons=[{
                    "text": f"Visa requires zero deductible but product has {ded}",
                    "evidence": req["evidence"]
                }]
            )
        return None
```

(Similar pattern for other rules)

### Step 4: Create rules package exports

Create `tools/rules/__init__.py`:
```python
"""Compliance rules package."""
from tools.rules.mandatory import MandatoryInsuranceRule
from tools.rules.deductible import NoDeductibleRule
from tools.rules.copayment import NoCopaymentRule
from tools.rules.moratorium import NoMoratoriumRule
from tools.rules.coverage import (
    MinimumCoverageRule,
    UnlimitedCoverageRule,
    ComprehensiveCoverageRule,
    CoversPublicHealthSystemRisksRule
)
from tools.rules.jurisdiction import AuthorizedInSpainRule, TravelInsuranceAcceptedRule
from tools.rules.payment import MonthlyPaymentsAcceptedRule, MustCoverFullPeriodRule

__all__ = [
    "MandatoryInsuranceRule",
    "NoDeductibleRule",
    "NoCopaymentRule",
    "NoMoratoriumRule",
    "MinimumCoverageRule",
    "UnlimitedCoverageRule",
    "ComprehensiveCoverageRule",
    "CoversPublicHealthSystemRisksRule",
    "AuthorizedInSpainRule",
    "TravelInsuranceAcceptedRule",
    "MonthlyPaymentsAcceptedRule",
    "MustCoverFullPeriodRule",
]
```

### Step 5: Create engine module

Create `tools/engine.py`:
```python
"""Compliance evaluation engine."""
from tools.rules import (
    MandatoryInsuranceRule,
    TravelInsuranceAcceptedRule,
    AuthorizedInSpainRule,
    NoDeductibleRule,
    ComprehensiveCoverageRule,
    CoversPublicHealthSystemRisksRule,
    UnlimitedCoverageRule,
    NoCopaymentRule,
    NoMoratoriumRule,
    MinimumCoverageRule,
    MonthlyPaymentsAcceptedRule,
    MustCoverFullPeriodRule,
)

# Rule order matters - terminal rules first
RULES = [
    MandatoryInsuranceRule(),
    TravelInsuranceAcceptedRule(),
    AuthorizedInSpainRule(),
    NoDeductibleRule(),
    ComprehensiveCoverageRule(),
    CoversPublicHealthSystemRisksRule(),
    UnlimitedCoverageRule(),
    NoCopaymentRule(),
    NoMoratoriumRule(),
    MinimumCoverageRule(),
    MonthlyPaymentsAcceptedRule(),
    MustCoverFullPeriodRule(),
]

def evaluate(visa: dict, product: dict) -> dict:
    """Evaluate visa/product compliance using all rules."""
    reasons = []
    missing = []
    status = "GREEN"
    
    for rule in RULES:
        result = rule.check(visa, product)
        if result is None:
            continue
        
        # Terminal rule (e.g., NOT_REQUIRED)
        if result.terminal:
            return {
                "visa_id": visa["id"],
                "product_id": product["id"],
                "status": result.status,
                "reasons": result.reasons,
                "missing": result.missing
            }
        
        # Merge results
        reasons.extend(result.reasons)
        missing.extend(result.missing)
        
        # Status priority: RED > UNKNOWN > YELLOW > GREEN
        if result.status == "RED":
            status = "RED"
        elif result.status == "UNKNOWN" and status not in ("RED",):
            status = "UNKNOWN"
        elif result.status == "YELLOW" and status == "GREEN":
            status = "YELLOW"
    
    # Final check: missing evidence means UNKNOWN
    if status == "GREEN" and missing:
        status = "UNKNOWN"
    
    return {
        "visa_id": visa["id"],
        "product_id": product["id"],
        "status": status,
        "reasons": reasons,
        "missing": missing
    }
```

### Step 6: Update build_mappings.py

Modify `tools/build_mappings.py`:
```python
import json
from pathlib import Path
from tools.engine import evaluate

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
PRODUCTS = ROOT / "data" / "products"
MAPPINGS = ROOT / "data" / "mappings"

MAPPINGS.mkdir(exist_ok=True)

def load_all(folder):
    files = []
    for p in folder.rglob("*.json"):
        files.append(json.loads(p.read_text(encoding="utf-8")))
    return files

visas = load_all(VISAS)
products = load_all(PRODUCTS)

for visa in visas:
    for product in products:
        result = evaluate(visa, product)
        out = MAPPINGS / f"{visa['id']}__{product['id']}.json"
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("Built", out)
```

### Step 7: Create basic test for rules

Create `tools/tests/test_rules.py`:
```python
"""Tests for compliance rules."""
import unittest
from tools.rules.mandatory import MandatoryInsuranceRule
from tools.rules.deductible import NoDeductibleRule

class TestMandatoryInsuranceRule(unittest.TestCase):
    def test_not_required(self):
        visa = {
            "id": "TEST",
            "requirements": [{"key": "insurance.mandatory", "value": False, "evidence": []}]
        }
        product = {"id": "PROD", "specs": {}}
        rule = MandatoryInsuranceRule()
        result = rule.check(visa, product)
        self.assertIsNotNone(result)
        self.assertEqual(result.status, "NOT_REQUIRED")
        self.assertTrue(result.terminal)

class TestNoDeductibleRule(unittest.TestCase):
    def test_pass(self):
        visa = {
            "id": "TEST",
            "requirements": [{"key": "insurance.no_deductible", "value": True, "evidence": []}]
        }
        product = {"id": "PROD", "specs": {"deductible": {"amount": 0}}}
        rule = NoDeductibleRule()
        result = rule.check(visa, product)
        self.assertIsNone(result)  # None means passed

    def test_fail(self):
        visa = {
            "id": "TEST",
            "requirements": [{"key": "insurance.no_deductible", "value": True, "evidence": []}]
        }
        product = {"id": "PROD", "specs": {"deductible": {"amount": 100}}}
        rule = NoDeductibleRule()
        result = rule.check(visa, product)
        self.assertIsNotNone(result)
        self.assertEqual(result.status, "RED")

if __name__ == "__main__":
    unittest.main()
```

### Step 8: Verify no regressions

Run: `python3 tools/build_mappings.py`
Expected: Same output files as before.

Run: `python3 tools/smoke.py`
Expected: Smoke check passed.

Run: `python3 tools/validate.py`
Expected: All data files valid.

Run: `python3 -m pytest tools/tests/test_rules.py -v`
Expected: All tests pass.

---

## Verification Plan

### Automated Tests
1. `python3 tools/validate.py` - Schema validation
2. `python3 tools/smoke.py` - Evidence integrity
3. `python3 -m pytest tools/tests/` - Unit tests
4. `npm run build:css && ls -la ui/style.css` - CSS build check

### Manual Verification
1. Run `npm run build:css`
2. Open `ui/index.html` in browser
3. Check: Colors, fonts, dark mode toggle, animations, all interactive elements
4. Compare with CDN version side-by-side if possible

### Commit Plan
1. Commit 1: "feat(frontend): add Tailwind build pipeline"
2. Commit 2: "refactor(backend): extract compliance rules to engine module"
3. Commit 3: "test(backend): add unit tests for compliance rules"
