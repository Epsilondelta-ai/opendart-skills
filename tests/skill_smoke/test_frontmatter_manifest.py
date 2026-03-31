from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "skills" / "opendart" / "references" / "frontmatter-manifest.md"
SKILLS = [
    ROOT / "skills" / "opendart",
    ROOT / "skills" / "opendart-disclosures",
    ROOT / "skills" / "opendart-periodic-reports",
    ROOT / "skills" / "opendart-financials",
    ROOT / "skills" / "opendart-equity",
    ROOT / "skills" / "opendart-material-events",
    ROOT / "skills" / "opendart-registration",
]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise AssertionError(f"Missing frontmatter in {path}")
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def parse_manifest(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `skills/"):
            continue
        cols = [c.strip().strip("`") for c in line.strip("|").split("|")]
        rows.append(cols)
    return rows


class FrontmatterManifestTests(unittest.TestCase):
    def test_manifest_rows_match_skill_frontmatter(self) -> None:
        rows = parse_manifest(MANIFEST)
        self.assertEqual(len(rows), len(SKILLS))
        for skill_dir, name, desc in rows:
            with self.subTest(skill_dir=skill_dir):
                data = parse_frontmatter(ROOT / skill_dir / "SKILL.md")
                self.assertEqual(data["name"], name)
                self.assertEqual(data["description"], desc)

    def test_each_skill_has_openai_metadata(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill.name):
                yaml_path = skill / "agents" / "openai.yaml"
                self.assertTrue(yaml_path.exists(), yaml_path)
                text = yaml_path.read_text(encoding="utf-8")
                data = parse_frontmatter(skill / "SKILL.md")
                self.assertIn("display_name:", text)
                self.assertIn("short_description:", text)
                self.assertIn("default_prompt:", text)
                self.assertIn(f'${data["name"]}', text)
