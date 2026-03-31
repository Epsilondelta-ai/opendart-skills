# Generic usage

## Portable usage model
The intended portable unit is the `skills/opendart/` directory.

If you copy this skill elsewhere, keep these subfolders together:
- `SKILL.md`
- `references/`
- `scripts/`
- `tests/` (optional but recommended)

## Minimum runtime use
- Read `SKILL.md`
- Use `references/` to route by family
- Use `scripts/opendart_cli.py` for corp-code, endpoint, cache, and live-call helpers

## Migration notes
Legacy top-level locations were intentionally collapsed into this single package.

| Old location | New location |
|---|---|
| `shared/opendart_common/*` | `skills/opendart/scripts/lib/*` |
| `core/opendart/manifests/*` | `skills/opendart/references/*` |
| `core/opendart/families/*` | `skills/opendart/references/family-*.md` |
| `tests/opendart_common/*` | `skills/opendart/tests/*` |
| `tests/opendart_live/*` | `skills/opendart/tests/test_live_lane.py` |
| `tests/skill_smoke/*` | `skills/opendart/tests/test_prompt_routing.py` and references |
| top-level `skills/opendart-*` specialist folders | folded into one `skills/opendart/` package |

If you previously referenced old repo-level paths directly, update them to the `skills/opendart/` equivalents.

Legacy path checker:
```bash
python3 skills/opendart/scripts/check_legacy_references.py <target-dir>
```
