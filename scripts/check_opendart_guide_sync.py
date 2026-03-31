#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shared.opendart_common.endpoint_catalog import EXPECTED_GUIDE_FAMILIES, FAMILY_TO_SKILL

GUIDE_MAP = ROOT / 'skills' / 'opendart' / 'references' / 'guide-family-map.md'


def parse_guide_rows() -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in GUIDE_MAP.read_text(encoding='utf-8').splitlines():
        if not line.startswith('| ') or line.startswith('|---'):
            continue
        cols = [part.strip().strip('`') for part in line.strip('|').split('|')]
        if len(cols) >= 2 and cols[0] != 'OpenDART guide family':
            rows[cols[0]] = cols[1]
    return rows


def check_sync() -> list[str]:
    rows = parse_guide_rows()
    expected = set(EXPECTED_GUIDE_FAMILIES)
    row_keys = set(rows)
    family_keys = set(FAMILY_TO_SKILL)
    errors: list[str] = []
    if row_keys != family_keys:
        errors.append(f'guide-family-map.md mismatch: rows={sorted(row_keys)} family_map={sorted(family_keys)}')
    if family_keys != expected:
        errors.append(f'expected-family mismatch: expected={sorted(expected)} actual={sorted(family_keys)}')
    return errors


def main() -> int:
    errors = check_sync()
    if errors:
        for error in errors:
            print(error)
        return 1
    print('OpenDART guide-family sync OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
