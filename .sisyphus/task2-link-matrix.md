# Task 2: Hub/Spoke Link Matrix + Per-Page Link Targets

## Link Formatting Rules
- Use absolute paths with trailing slashes for content pages: `/posts/.../`, `/guides/.../`, `/traps/.../`, `/visas/.../`.
- Use `/ui/` and `/methodology/` as-is (no anchors).
- Use default Hugo paths; no frontmatter url/slug/permalink overrides exist.

## Hub/Spoke Topology (Recommended)

**Primary hubs**
- Regional hubs: `/posts/digital-nomad-insurance-europe/`, `/posts/digital-nomad-insurance-asia/`, `/posts/digital-nomad-insurance-americas/`
- Visa country hubs (visa-type hubs): `/visas/spain/digital-nomad-visa/`, `/visas/portugal/temporary-stay-visa-for-remote-work-e11/`, `/visas/germany/freelance-visa-national-d/`, `/visas/thailand/digital-nomad-visa-dtv/`, `/visas/malta/nomad-residence-permit/`, `/visas/costa-rica/digital-nomad-visa/`

**Primary spokes**
- Route posts: country-specific posts in `content/posts/`
- Visa route pages: specific route pages in `content/visas/**/index.md`
- Traps: risk-focused posts in `content/traps/`
- Guides: workflow/definitions in `content/guides/`

## Required Link Targets by Content Type

| Content Type | Required Links |
|---|---|
| Route post | 1 visa spoke + 1 trap + 1 regional hub + `/ui/` |
| Trap | 1 route post + 1 visa spoke + `/methodology/` |
| Guide | 1 route post + 1 visa spoke + `/ui/` |
| Visa spoke | 1 route post + 1 visa country hub + `/ui/` |
| Regional hub | all country route posts + `/ui/` |

Exception: If a route does not require insurance (e.g., Thailand DTV), the route post can replace the trap link with guide links to maintain minimum 5 internal links.

## Per-Route Mapping

### Spain
- Route post: `/posts/spain-dnv-insurance/`
- Visa spoke: `/visas/spain/digital-nomad-visa/consulate-via-bls-london/`
- Visa country hub: `/visas/spain/digital-nomad-visa/`
- Regional hub: `/posts/digital-nomad-insurance-europe/`
- Trap link target: `/traps/spain-dnv-insurance-mistakes/`
- Guide link target: `/guides/how-to-read-results/`

### Portugal
- Route post: `/posts/portugal-dnv-insurance/`
- Visa spoke: `/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/`
- Visa country hub: `/visas/portugal/temporary-stay-visa-for-remote-work-e11/`
- Regional hub: `/posts/digital-nomad-insurance-europe/`
- Trap link target: `/traps/germany-travel-insurance-rejected/`
- Guide link target: `/guides/how-to-read-results/`

### Germany
- Route post: `/posts/germany-freelance-insurance/`
- Visa spoke: `/visas/germany/freelance-visa-national-d/embassy-london/`
- Visa country hub: `/visas/germany/freelance-visa-national-d/`
- Regional hub: `/posts/digital-nomad-insurance-europe/`
- Trap link target: `/traps/germany-travel-insurance-rejected/`
- Guide link target: `/guides/how-to-choose-dnv-insurance/`

### Thailand
- Route post: `/posts/thailand-dtv-insurance/`
- Visa spoke: `/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/`
- Visa country hub: `/visas/thailand/digital-nomad-visa-dtv/`
- Regional hub: `/posts/digital-nomad-insurance-asia/`
- Trap link target: _none_ (insurance = NOT_REQUIRED for DTV; no relevant trap)
- Guide link targets: `/guides/compliance-status-meaning/`, `/guides/how-to-read-results/`

### Malta
- Route post: `/posts/malta-nomad-insurance/`
- Visa spoke: `/visas/malta/nomad-residence-permit/residency-malta-agency/`
- Visa country hub: `/visas/malta/nomad-residence-permit/`
- Regional hub: `/posts/digital-nomad-insurance-europe/`
- Trap link target: `/traps/malta-nomad-monthly-payments/`
- Guide link target: `/guides/how-to-read-results/`

### Costa Rica
- Route post: `/posts/costa-rica-dn-insurance/`
- Visa spoke: `/visas/costa-rica/digital-nomad-visa/executive-decree-43619/`
- Visa country hub: `/visas/costa-rica/digital-nomad-visa/`
- Regional hub: `/posts/digital-nomad-insurance-americas/`
- Trap link target: `/traps/germany-travel-insurance-rejected/` (generic rejection pitfalls; no Costa Rica-specific trap)
- Guide link target: `/guides/how-to-read-results/`

## Per-Page Link Targets (Ready to Apply)

> Minimum 5 internal links per page. Format: **required** links first, then _bonus_ links.

### Route Posts (5 links each)
- `/posts/spain-dnv-insurance/` -> `/visas/spain/digital-nomad-visa/consulate-via-bls-london/`, `/traps/spain-dnv-insurance-mistakes/`, `/posts/digital-nomad-insurance-europe/`, `/ui/`, _`/guides/how-to-read-results/`_
- `/posts/portugal-dnv-insurance/` -> `/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/`, `/traps/germany-travel-insurance-rejected/`, `/posts/digital-nomad-insurance-europe/`, `/ui/`, _`/guides/schengen-30000-insurance/`_
- `/posts/germany-freelance-insurance/` -> `/visas/germany/freelance-visa-national-d/embassy-london/`, `/traps/germany-travel-insurance-rejected/`, `/posts/digital-nomad-insurance-europe/`, `/ui/`, _`/guides/how-to-choose-dnv-insurance/`_
- `/posts/thailand-dtv-insurance/` -> `/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/`, `/posts/digital-nomad-insurance-asia/`, `/ui/`, `/guides/compliance-status-meaning/`, _`/guides/how-to-read-results/`_ _(no trap — insurance NOT_REQUIRED for DTV)_
- `/posts/malta-nomad-insurance/` -> `/visas/malta/nomad-residence-permit/residency-malta-agency/`, `/traps/malta-nomad-monthly-payments/`, `/posts/digital-nomad-insurance-europe/`, `/ui/`, _`/guides/how-to-read-results/`_
- `/posts/costa-rica-dn-insurance/` -> `/visas/costa-rica/digital-nomad-visa/executive-decree-43619/`, `/traps/germany-travel-insurance-rejected/`, `/posts/digital-nomad-insurance-americas/`, `/ui/`, _`/guides/how-to-read-results/`_

### Comparison/Rejected Posts (5 links each)
- `/posts/safetywing-spain-dnv-rejected/` -> `/visas/spain/digital-nomad-visa/consulate-via-bls-london/`, `/posts/spain-dnv-insurance/`, `/traps/spain-dnv-insurance-mistakes/`, `/ui/`, _`/guides/how-to-read-results/`_
- `/posts/safetywing-vs-worldnomads-vs-genki/` -> `/visas/spain/digital-nomad-visa/consulate-via-bls-london/`, `/posts/spain-dnv-insurance/`, `/posts/germany-freelance-insurance/`, `/ui/`, _`/guides/how-to-choose-dnv-insurance/`_

### Traps (5 links each)
- `/traps/spain-dnv-insurance-mistakes/` -> `/posts/spain-dnv-insurance/`, `/visas/spain/digital-nomad-visa/consulate-via-bls-london/`, `/methodology/`, _`/guides/how-to-read-results/`_, _`/posts/digital-nomad-insurance-europe/`_
- `/traps/spain-dnv-coverage-cap-trap/` -> `/posts/spain-dnv-insurance/`, `/visas/spain/digital-nomad-visa/consulate-via-bls-london/`, `/methodology/`, _`/guides/schengen-30000-insurance/`_, _`/posts/digital-nomad-insurance-europe/`_
- `/traps/germany-travel-insurance-rejected/` -> `/posts/germany-freelance-insurance/`, `/visas/germany/freelance-visa-national-d/embassy-london/`, `/methodology/`, _`/guides/how-to-choose-dnv-insurance/`_, _`/posts/digital-nomad-insurance-europe/`_
- `/traps/malta-nomad-monthly-payments/` -> `/posts/malta-nomad-insurance/`, `/visas/malta/nomad-residence-permit/residency-malta-agency/`, `/methodology/`, _`/guides/how-to-read-results/`_, _`/posts/digital-nomad-insurance-europe/`_

### Guides (5 links each)
- `/guides/how-to-read-results/` -> `/posts/spain-dnv-insurance/`, `/visas/spain/digital-nomad-visa/consulate-via-bls-london/`, `/ui/`, _`/traps/spain-dnv-insurance-mistakes/`_, _`/posts/digital-nomad-insurance-europe/`_
- `/guides/how-to-choose-dnv-insurance/` -> `/posts/germany-freelance-insurance/`, `/visas/germany/freelance-visa-national-d/embassy-london/`, `/ui/`, _`/traps/germany-travel-insurance-rejected/`_, _`/posts/digital-nomad-insurance-europe/`_
- `/guides/compliance-status-meaning/` -> `/posts/thailand-dtv-insurance/`, `/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/`, `/ui/`, _`/posts/digital-nomad-insurance-asia/`_, _`/guides/how-to-read-results/`_
- `/guides/schengen-30000-insurance/` -> `/posts/spain-dnv-insurance/`, `/visas/spain/digital-nomad-visa/consulate-via-bls-london/`, `/ui/`, _`/traps/spain-dnv-coverage-cap-trap/`_, _`/posts/digital-nomad-insurance-europe/`_

### Visa Spokes (5 links each)
- `/visas/spain/digital-nomad-visa/consulate-via-bls-london/` -> `/posts/spain-dnv-insurance/`, `/visas/spain/digital-nomad-visa/`, `/ui/`, _`/traps/spain-dnv-insurance-mistakes/`_, _`/guides/how-to-read-results/`_
- `/visas/portugal/temporary-stay-visa-for-remote-work-e11/vfs-global-china/` -> `/posts/portugal-dnv-insurance/`, `/visas/portugal/temporary-stay-visa-for-remote-work-e11/`, `/ui/`, _`/guides/schengen-30000-insurance/`_, _`/posts/digital-nomad-insurance-europe/`_
- `/visas/germany/freelance-visa-national-d/embassy-london/` -> `/posts/germany-freelance-insurance/`, `/visas/germany/freelance-visa-national-d/`, `/ui/`, _`/traps/germany-travel-insurance-rejected/`_, _`/guides/how-to-choose-dnv-insurance/`_
- `/visas/thailand/digital-nomad-visa-dtv/thai-e-visa/` -> `/posts/thailand-dtv-insurance/`, `/visas/thailand/digital-nomad-visa-dtv/`, `/ui/`, _`/guides/compliance-status-meaning/`_, _`/posts/digital-nomad-insurance-asia/`_
- `/visas/malta/nomad-residence-permit/residency-malta-agency/` -> `/posts/malta-nomad-insurance/`, `/visas/malta/nomad-residence-permit/`, `/ui/`, _`/traps/malta-nomad-monthly-payments/`_, _`/guides/how-to-read-results/`_
- `/visas/costa-rica/digital-nomad-visa/executive-decree-43619/` -> `/posts/costa-rica-dn-insurance/`, `/visas/costa-rica/digital-nomad-visa/`, `/ui/`, _`/guides/how-to-read-results/`_, _`/posts/digital-nomad-insurance-americas/`_

### Regional Hubs (5 links each)
- `/posts/digital-nomad-insurance-europe/` -> `/posts/spain-dnv-insurance/`, `/posts/portugal-dnv-insurance/`, `/posts/germany-freelance-insurance/`, `/posts/malta-nomad-insurance/`, `/ui/`, _`/visas/spain/digital-nomad-visa/`_
- `/posts/digital-nomad-insurance-asia/` -> `/posts/thailand-dtv-insurance/`, `/ui/`, _`/visas/thailand/digital-nomad-visa-dtv/`_, _`/guides/compliance-status-meaning/`_, _`/guides/how-to-read-results/`_
- `/posts/digital-nomad-insurance-americas/` -> `/posts/costa-rica-dn-insurance/`, `/ui/`, _`/visas/costa-rica/digital-nomad-visa/`_, _`/guides/how-to-read-results/`_, _`/guides/how-to-choose-dnv-insurance/`_
