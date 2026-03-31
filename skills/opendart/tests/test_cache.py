from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.cache import corp_code_cache_status, corp_code_ttl_days, corp_code_xml_path, write_corp_code_metadata


class CacheTests(unittest.TestCase):
    def test_missing_cache_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            status = corp_code_cache_status(tmpdir)
            self.assertTrue(status['stale'])
            self.assertEqual(status['reason'], 'missing_xml_cache')

    def test_missing_metadata_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            corp_code_xml_path(tmpdir).write_text('<result></result>', encoding='utf-8')
            status = corp_code_cache_status(tmpdir)
            self.assertTrue(status['stale'])
            self.assertEqual(status['reason'], 'missing_metadata')

    def test_expired_metadata_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            corp_code_xml_path(tmpdir).write_text('<result></result>', encoding='utf-8')
            write_corp_code_metadata(tmpdir, fetched_at=datetime.now(UTC) - timedelta(days=corp_code_ttl_days() + 1))
            status = corp_code_cache_status(tmpdir)
            self.assertTrue(status['stale'])
            self.assertEqual(status['reason'], 'ttl_expired')
