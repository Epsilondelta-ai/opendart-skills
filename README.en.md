# opendart-skills

[한국어](README.md) | [English](README.en.md)

The main deliverable in this repository is the **self-contained OpenDART skill package** at `skills/opendart/`.

In practice, the repository is centered on:

```text
skills/
  opendart/
    SKILL.md
    references/
    scripts/
    tests/
```

## Core rules
- `skills/opendart/` is the main package.
- It does not depend on higher-level `shared/`, `core/`, or `adapters/` layers.
- Helper code lives inside `skills/opendart/scripts/`.
- OpenDART family specialization is handled internally through routing and references instead of separate top-level skills.

## Coverage
- disclosure information
- key information from periodic reports
- financial information from periodic reports
- utility / query-download workflows
- equity disclosure information
- major event report information
- registration statement information

## Main entry points
- skill instructions: `skills/opendart/SKILL.md`
- references: `skills/opendart/references/`
- helper scripts: `skills/opendart/scripts/`
- tests: `skills/opendart/tests/`

## CLI examples
```bash
python3 skills/opendart/scripts/opendart_cli.py --help
python3 skills/opendart/scripts/opendart_cli.py corp-code status
python3 skills/opendart/scripts/check_guide_sync.py
```

## Verification
```bash
python3 -m unittest discover skills/opendart/tests
python3 -m compileall skills/opendart/scripts
python3 skills/opendart/scripts/check_guide_sync.py
```

Live smoke lane:
```bash
OPENDART_API_KEY=... python3 -m unittest discover skills/opendart/tests -p 'test_live_lane.py'
```

## Portability
If you want to reuse this elsewhere, the intended unit to copy is the `skills/opendart/` directory itself.

## Migration notes
- old top-level helper locations such as `shared/`, `core/`, `adapters/`, and repo-level `tests/` were collapsed into `skills/opendart/`.
- if you previously referenced repo-level paths directly, switch to the equivalents under `skills/opendart/`.
- the intended portable unit is now the `skills/opendart/` directory itself.

Legacy path checker:
```bash
python3 skills/opendart/scripts/check_legacy_references.py <target-dir>
```
