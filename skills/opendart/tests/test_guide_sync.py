from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_guide_sync import check_sync


class GuideSyncTests(unittest.TestCase):
    def test_guide_sync_has_no_errors(self) -> None:
        self.assertEqual(check_sync(), [])
