import unittest

from helpers import REPO_ROOT
from architecture import parse_scopes, parse_uses

TEMPLATES = REPO_ROOT / "plugin" / "templates" / "development"


def read(name):
    return (TEMPLATES / name).read_text(encoding="utf-8")


class DevelopmentTemplatesTest(unittest.TestCase):
    def test_all_templates_exist(self):
        for name in ("architecture.md", "scope.md", "interfaces.md", "interface.md", "catalog.md"):
            with self.subTest(name=name):
                self.assertTrue((TEMPLATES / name).is_file())

    def test_architecture_template_tables_are_valid_and_empty(self):
        text = read("architecture.md")
        self.assertEqual(parse_scopes(text), ([], []))
        self.assertEqual(parse_uses(text), ([], []))

    def test_architecture_template_shows_required_reading_and_sub_scopes(self):
        text = read("architecture.md")
        self.assertIn("Required reading", text)
        self.assertIn("plugins/patient", text)
        self.assertIn("## Required on use", text)

    def test_scope_template_has_responsibilities_table(self):
        text = read("scope.md")
        self.assertIn("| Concern | Owner | Others do | Others don't | Details |", text)
        self.assertIn("## Rules", text)
        self.assertEqual(parse_uses(text), ([], []))

    def test_catalog_template_has_building_block_table(self):
        self.assertIn("| Building block | Purpose | Use when | Details |", read("catalog.md"))

    def test_interfaces_templates(self):
        self.assertIn("| File | Covers |", read("interfaces.md"))
        self.assertIn("## Use", read("interface.md"))
