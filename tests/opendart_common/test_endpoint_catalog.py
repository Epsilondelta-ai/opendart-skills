from __future__ import annotations

import json
import unittest
from pathlib import Path

from shared.opendart_common.endpoint_catalog import CATALOG_SPLIT_THRESHOLD, ENDPOINTS, EXPECTED_GUIDE_FAMILIES, FAMILY_TO_SKILL, list_endpoints

ROOT = Path(__file__).resolve().parents[2]
PROMPT_MATRIX = ROOT / 'tests' / 'skill_smoke' / 'prompt_matrix.json'
GUIDE_MAP = ROOT / 'skills' / 'opendart' / 'references' / 'guide-family-map.md'


def guide_map_rows() -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in GUIDE_MAP.read_text(encoding='utf-8').splitlines():
        if not line.startswith('| ') or line.startswith('|---'):
            continue
        cols = [part.strip().strip('`') for part in line.strip('|').split('|')]
        if len(cols) >= 2 and cols[0] != 'OpenDART guide family':
            rows[cols[0]] = cols[1]
    return rows


class EndpointCatalogTests(unittest.TestCase):
    def test_expected_families_are_declared(self) -> None:
        self.assertEqual(set(EXPECTED_GUIDE_FAMILIES), set(FAMILY_TO_SKILL))

    def test_specialist_families_have_owned_endpoints(self) -> None:
        for family, skill in FAMILY_TO_SKILL.items():
            if family == '활용마당':
                continue
            with self.subTest(family=family):
                items = [item for item in ENDPOINTS.values() if item.family == family and item.skill == skill]
                self.assertTrue(items)

    def test_guide_map_matches_family_to_skill(self) -> None:
        rows = guide_map_rows()
        self.assertEqual(rows, FAMILY_TO_SKILL)

    def test_prompt_matrix_covers_each_family(self) -> None:
        entries = json.loads(PROMPT_MATRIX.read_text(encoding='utf-8'))
        families = {entry['family'] for entry in entries if entry['family'] != 'umbrella'}
        self.assertTrue(set(FAMILY_TO_SKILL).issubset(families | {'활용마당'}))

    def test_filtering_by_skill(self) -> None:
        items = list_endpoints(skill='opendart-financials')
        self.assertGreaterEqual(len(items), 2)
        self.assertTrue(all(item.skill == 'opendart-financials' for item in items))

    def test_catalog_split_threshold_is_numeric(self) -> None:
        self.assertIsInstance(CATALOG_SPLIT_THRESHOLD, int)
        self.assertGreaterEqual(CATALOG_SPLIT_THRESHOLD, len(ENDPOINTS))
