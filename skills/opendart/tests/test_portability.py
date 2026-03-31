from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PortabilityTests(unittest.TestCase):
    def test_skill_directory_runs_when_copied(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'opendart'
            shutil.copytree(ROOT, target)
            cli = target / 'scripts' / 'opendart_cli.py'
            guide = target / 'scripts' / 'check_guide_sync.py'

            help_run = subprocess.run(['python3', str(cli), '--help'], capture_output=True, text=True)
            self.assertEqual(help_run.returncode, 0, help_run.stderr)
            self.assertIn('Self-contained OpenDART skill helper CLI', help_run.stdout)

            sync_run = subprocess.run(['python3', str(guide)], capture_output=True, text=True)
            self.assertEqual(sync_run.returncode, 0, sync_run.stderr)
            self.assertIn('OpenDART family sync OK', sync_run.stdout)
