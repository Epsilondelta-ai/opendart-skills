from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from shared.opendart_common.cli import main
from shared.opendart_common.cache import write_corp_code_metadata


class CliTests(unittest.TestCase):
    def test_corp_code_search_reports_missing_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            buffer = StringIO()
            with redirect_stdout(buffer):
                code = main(['--cache-dir', tmpdir, 'corp-code', 'search', '--name', '삼성'])
            self.assertEqual(code, 2)
            payload = json.loads(buffer.getvalue())
            self.assertIn('missing', payload['message'])

    def test_corp_code_status_reports_stale_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'corpCode.xml').write_text('<result></result>', encoding='utf-8')
            write_corp_code_metadata(tmpdir, fetched_at='2000-01-01T00:00:00+00:00', ttl_seconds=60)
            buffer = StringIO()
            with redirect_stdout(buffer):
                code = main(['--cache-dir', tmpdir, 'corp-code', 'status'])
            self.assertEqual(code, 0)
            payload = json.loads(buffer.getvalue())
            self.assertTrue(payload['stale'])
            self.assertIn('Refresh', payload['hint'])

    def test_company_reports_missing_key(self) -> None:
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = main(['company', '--corp-code', '00126380'])
        self.assertEqual(code, 2)
        payload = json.loads(buffer.getvalue())
        self.assertIn('OPENDART_API_KEY', payload['message'])
