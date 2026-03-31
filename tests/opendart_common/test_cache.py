from __future__ import annotations

import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from shared.opendart_common.cache import corp_code_cache_status, corp_code_ttl_days, write_corp_code_metadata


class CacheTests(unittest.TestCase):
    def test_missing_cache_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            status = corp_code_cache_status(tmpdir)
            self.assertTrue(status["stale"])
            self.assertEqual(status["reason"], "missing_xml_cache")

    def test_missing_metadata_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "corpCode.xml").write_text("<result></result>", encoding="utf-8")
            status = corp_code_cache_status(tmpdir)
            self.assertTrue(status["stale"])
            self.assertEqual(status["reason"], "missing_metadata")

    def test_expired_metadata_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "corpCode.xml").write_text("<result></result>", encoding="utf-8")
            write_corp_code_metadata(tmpdir, fetched_at=datetime.now(UTC) - timedelta(days=corp_code_ttl_days() + 1))
            status = corp_code_cache_status(tmpdir)
            self.assertTrue(status["stale"])
            self.assertEqual(status["reason"], "ttl_expired")

    def test_fresh_metadata_is_not_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "corpCode.xml").write_text("<result></result>", encoding="utf-8")
            write_corp_code_metadata(tmpdir, fetched_at=datetime.now(UTC))
            status = corp_code_cache_status(tmpdir)
            self.assertFalse(status["stale"])
            self.assertEqual(status["reason"], "fresh")
