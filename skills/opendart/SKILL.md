---
name: opendart
description: Generic OpenDART skill for corp_code resolution, disclosure search, periodic-report facts, financial data, equity disclosures, material events, and registration statements.
---

# OpenDART

This is a self-contained generic skill for working with OpenDART.

## Use when
- You need OpenDART auth or `corp_code` guidance.
- You need to route a request across OpenDART families.
- You need disclosure, periodic-report, financial, equity, material-event, or registration-statement workflows.
- You want repeatable helper-script support from inside the skill package itself.

## Internal routing
Use the references in this skill instead of depending on separate top-level specialist skills.

1. `references/service-overview.md` — OpenDART mental model
2. `references/auth-corpcode-errors.md` — auth, `corp_code`, cache, and status handling
3. `references/family-map.md` — OpenDART family ownership inside this single skill
4. `references/routing-matrix.md` — prompt-to-family routing
5. `references/endpoint-catalog.md` — representative endpoint catalog
6. `references/generic-usage.md` — how to use/copy this skill as a portable package
7. `references/family-*.md` — family-specific notes and examples

## Script entry points
- `python3 skills/opendart/scripts/opendart_cli.py --help`
- `python3 skills/opendart/scripts/check_guide_sync.py`

## Guardrails
- Never store or echo a real `crtfc_key` in repo files.
- Treat this skill directory as the portable package; do not depend on removed top-level helper layers.
- Keep new logic under `scripts/` and new reference truth under `references/`.
