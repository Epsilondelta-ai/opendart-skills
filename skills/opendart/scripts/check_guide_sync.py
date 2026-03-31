#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lib.endpoint_catalog import EXPECTED_GUIDE_FAMILIES, FAMILY_TO_SECTION

ROOT = Path(__file__).resolve().parents[1]
GUIDE_MAP = ROOT / 'references' / 'family-map.md'


def parse_guide_rows() -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in GUIDE_MAP.read_text(encoding='utf-8').splitlines():
        if not line.startswith('| ') or line.startswith('|---'):
            continue
        cols = [part.strip().strip('`') for part in line.strip('|').split('|')]
        if len(cols) >= 2 and cols[0] != 'Family':
            rows[cols[0]] = cols[1]
    return rows


def check_sync() -> list[str]:
    rows = parse_guide_rows()
    row_keys = set(rows)
    family_keys = set(FAMILY_TO_SECTION)
    expected = set(EXPECTED_GUIDE_FAMILIES)
    errors: list[str] = []
    if row_keys != family_keys:
        errors.append(f'family-map.md mismatch: rows={sorted(row_keys)} expected={sorted(family_keys)}')
    if family_keys != expected:
        errors.append(f'expected-family mismatch: expected={sorted(expected)} actual={sorted(family_keys)}')
    return errors


def main() -> int:
    errors = check_sync()
    if errors:
        for error in errors:
            print(error)
        return 1
    print('OpenDART family sync OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
