#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

LEGACY_MAP = {
    'shared/opendart_common/api.py': 'skills/opendart/scripts/lib/api.py',
    'shared/opendart_common/cache.py': 'skills/opendart/scripts/lib/cache.py',
    'shared/opendart_common/cli.py': 'skills/opendart/scripts/lib/cli.py',
    'shared/opendart_common/corpcode.py': 'skills/opendart/scripts/lib/corpcode.py',
    'shared/opendart_common/endpoint_catalog.py': 'skills/opendart/scripts/lib/endpoint_catalog.py',
    'shared/opendart_common/errors.py': 'skills/opendart/scripts/lib/errors.py',
    'scripts/check_opendart_guide_sync.py': 'skills/opendart/scripts/check_guide_sync.py',
    'tests/opendart_common/': 'skills/opendart/tests/',
    'tests/opendart_live/test_live_lane.py': 'skills/opendart/tests/test_live_lane.py',
    'tests/skill_smoke/': 'skills/opendart/tests/ and skills/opendart/references/',
    'skills/opendart-disclosures/': 'skills/opendart/references/family-disclosures.md',
    'skills/opendart-periodic-reports/': 'skills/opendart/references/family-periodic-reports.md',
    'skills/opendart-financials/': 'skills/opendart/references/family-financials.md',
    'skills/opendart-equity/': 'skills/opendart/references/family-equity.md',
    'skills/opendart-material-events/': 'skills/opendart/references/family-material-events.md',
    'skills/opendart-registration/': 'skills/opendart/references/family-registration.md',
    'core/opendart/manifests/': 'skills/opendart/references/',
    'core/opendart/families/': 'skills/opendart/references/family-*.md',
    'adapters/codex/': 'use the self-contained skills/opendart/ package instead',
}

TEXT_SUFFIXES = {'.md', '.txt', '.py', '.json', '.yaml', '.yml', '.toml', '.sh'}
IGNORE_NAMES = {'legacy-path-map.md', 'generic-usage.md', 'check_legacy_references.py', 'test_legacy_paths.py'}


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    matches: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return matches
    for line_no, line in enumerate(text.splitlines(), start=1):
        for old, new in LEGACY_MAP.items():
            if old in line:
                matches.append((line_no, old, new))
    return matches


def scan_tree(root: Path) -> list[str]:
    findings: list[str] = []
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name in IGNORE_NAMES:
            continue
        if '.git' in path.parts or '.omx' in path.parts or '__pycache__' in path.parts:
            continue
        for line_no, old, new in scan_file(path):
            findings.append(f'{path}:{line_no}: legacy path `{old}` -> `{new}`')
    return findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Scan a directory for deleted legacy OpenDART path references.')
    parser.add_argument('target', nargs='?', default='.', help='directory to scan')
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.target).resolve()
    findings = scan_tree(root)
    if findings:
        for item in findings:
            print(item)
        return 1
    print('No legacy OpenDART path references found.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
