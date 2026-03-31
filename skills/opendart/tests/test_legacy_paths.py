from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_legacy_references import scan_tree


class LegacyPathTests(unittest.TestCase):
    def test_checker_detects_old_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / 'sample.md'
            sample.write_text('Use shared/opendart_common/api.py and skills/opendart-financials/ next.', encoding='utf-8')
            findings = scan_tree(Path(tmpdir))
            self.assertEqual(len(findings), 2)
            self.assertTrue(any('shared/opendart_common/api.py' in item for item in findings))
            self.assertTrue(any('skills/opendart-financials/' in item for item in findings))

    def test_checker_ignores_clean_tree(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sample = Path(tmpdir) / 'sample.md'
            sample.write_text('Use skills/opendart/scripts/lib/api.py instead.', encoding='utf-8')
            self.assertEqual(scan_tree(Path(tmpdir)), [])
