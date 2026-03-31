from __future__ import annotations

import json
import sys
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from lib.cache import write_corp_code_metadata
from lib.cli import main


class CliTests(unittest.TestCase):
    def test_corp_code_search_reports_missing_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            buffer = StringIO()
            with patch.dict('os.environ', {}, clear=True):
                with redirect_stdout(buffer):
                    code = main(['--cache-dir', tmpdir, 'corp-code', 'search', '--name', '삼성'])
            self.assertEqual(code, 2)
            self.assertIn('missing corp-code cache', json.loads(buffer.getvalue())['message'])

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

    def test_corp_code_search_reports_unrepairable_invalid_cache(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, 'corpCode.xml').write_text('<result><list><corp_name>AT&T</corp_name></list></result>', encoding='utf-8')
            write_corp_code_metadata(tmpdir)
            buffer = StringIO()
            with patch.dict('os.environ', {}, clear=True):
                with redirect_stdout(buffer):
                    code = main(['--cache-dir', tmpdir, 'corp-code', 'search', '--name', 'AT&T'])
            self.assertEqual(code, 2)
            payload = json.loads(buffer.getvalue())
            self.assertIn('could not be repaired', payload['message'])
            self.assertIn('auto-refresh', payload['hint'])

    def test_company_reports_missing_key(self) -> None:
        buffer = StringIO()
        with patch.dict('os.environ', {}, clear=True):
            with redirect_stdout(buffer):
                code = main(['company', '--corp-code', '00126380'])
        self.assertEqual(code, 2)
        self.assertIn('OPENDART_API_KEY', json.loads(buffer.getvalue())['message'])
