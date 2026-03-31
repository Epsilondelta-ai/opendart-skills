from __future__ import annotations

import unittest

from scripts.check_opendart_guide_sync import check_sync


class GuideSyncTests(unittest.TestCase):
    def test_guide_sync_has_no_errors(self) -> None:
        self.assertEqual(check_sync(), [])
