from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.endpoint_catalog import ENDPOINTS, EXPECTED_GUIDE_FAMILIES, FAMILY_TO_SECTION, list_endpoints

ROOT = Path(__file__).resolve().parents[1]


class EndpointCatalogTests(unittest.TestCase):
    def test_major_families_are_covered(self) -> None:
        families = {item.family for item in ENDPOINTS.values()}
        self.assertTrue(set(EXPECTED_GUIDE_FAMILIES).issubset(families))

    def test_family_to_section_covers_full_scope(self) -> None:
        self.assertEqual(FAMILY_TO_SECTION['활용마당'], 'financials')
        self.assertEqual(FAMILY_TO_SECTION['증권신고서 주요정보'], 'registration')

    def test_filtering_by_section(self) -> None:
        items = list_endpoints(section='financials')
        self.assertGreaterEqual(len(items), 3)
        self.assertTrue(all(item.section == 'financials' for item in items))

    def test_reference_catalog_mentions_all_expected_families(self) -> None:
        text = (ROOT / 'references' / 'endpoint-catalog.md').read_text(encoding='utf-8')
        for family in EXPECTED_GUIDE_FAMILIES:
            with self.subTest(family=family):
                self.assertIn(family, text)
